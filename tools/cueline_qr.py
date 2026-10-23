#!/usr/bin/env python3
"""Make a Cueline script link and QR code.

Usage:  python3 cueline_qr.py "Script title" script.txt out.png
        (use "-" as the script path to read the script from stdin)

Prints the link. Writes a QR code PNG when it fits in one code; otherwise says so,
and the link can be sent instead (Cueline > Scan script > paste the link).
"""
import base64
import json
import sys
import zlib

APP_URL = "https://charliefehr09-longheld.github.io/Cueline/"


def make_link(title: str, body: str) -> str:
    data = json.dumps({"t": title, "b": body}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    comp = zlib.compressobj(9, zlib.DEFLATED, -15)  # raw DEFLATE, matches the app's "deflate-raw"
    raw = comp.compress(data) + comp.flush()
    return APP_URL + "#cue1=" + base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def make_qr(link: str, path: str) -> bool:
    import qrcode
    from qrcode.exceptions import DataOverflowError
    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(link, optimize=0)
        qr.make(fit=True)
    except DataOverflowError:
        return False
    qr.make_image(fill_color="black", back_color="white").save(path)
    return True


if __name__ == "__main__":
    title, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
    body = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    link = make_link(title, body.strip("\n"))
    print(link)
    print("QR saved to " + out if make_qr(link, out) else "Too long for one QR code; send the link instead.", file=sys.stderr)
