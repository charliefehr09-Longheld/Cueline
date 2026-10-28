#!/usr/bin/env python3
"""Make a Cueline script link and QR code.

Usage:  python3 cueline_qr.py "Script title" script.txt out.png
        (use "-" as the script path to read the script from stdin)

Prints the link (for pasting). Writes a QR code PNG in the compact CUE2 form when it fits in one code; otherwise says so,
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


B45 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"


def b45(raw: bytes) -> str:
    out = []
    for i in range(0, len(raw) - 1, 2):
        n = raw[i] * 256 + raw[i + 1]
        c, n = n % 45, n // 45
        d, e = n % 45, n // 45
        out += [B45[c], B45[d], B45[e]]
    if len(raw) % 2:
        n = raw[-1]
        out += [B45[n % 45], B45[n // 45]]
    return "".join(out)


def make_compact(title: str, body: str) -> str:
    """QR payload: 'CUE2:' + base45 of the same compressed JSON. Fits QR alphanumeric mode, so the code is less dense."""
    data = json.dumps({"t": title, "b": body}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    comp = zlib.compressobj(9, zlib.DEFLATED, -15)
    return "CUE2:" + b45(comp.compress(data) + comp.flush())


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


def make_qr_compact(title: str, body: str, path: str) -> bool:
    return make_qr(make_compact(title, body), path)


if __name__ == "__main__":
    title, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
    body = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    body = body.strip("\n")
    link = make_link(title, body)
    print(link)
    ok = make_qr_compact(title, body, out)   # the QR uses the compact form; the printed link is for pasting
    print("QR saved to " + out if ok else "Too long for one QR code; send the link instead.", file=sys.stderr)
