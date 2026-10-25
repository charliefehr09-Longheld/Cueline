# Cueline

A knob-driven teleprompter for iPad and laptop.

- **Scroll mode:** rolling text, speed on the knob, mirror, text size.
- **Take mode:** one line at a time, knob press to start and stop takes, long press for good, double press for scratch, and a counter showing how many lines you've got.
- **Marks only:** Cueline listens for each attempt. Press the knob once for good, twice for scratch, nothing before you speak. Takes are found from the audio, so you never start or stop anything mid-session. (Settings › Takes.)
- **Filming queue:** tap + on scripts to queue them; Prompt rolls from one into the next on the knob, with one recording and one package for the whole day.
- **Session recording:** records the audio of a whole shoot on the iPad. If iPadOS pauses the recording (screen lock, a call), the pause is filled with silence so the file stays in real time, and each pause is listed in the package. When you wrap, Cueline cuts out the good takes (or everything except scratch takes, or keeps the full recording), sends it to AssemblyAI, compares what you said with the script, and saves one package: `session.json` for indexing, a readable transcript with slates written in, captions, a CSV and DaVinci Resolve markers, plus selects-only versions.
- **Send to iPad:** any script becomes a QR code or link. Tap **Scan script** in Cueline on the iPad to load it.

## Install on the iPad

Open the site in Safari, tap Share › **Add to Home Screen**, and launch Cueline from its icon. It runs full screen and works offline (transcription needs a connection).

## Privacy

Scripts, take logs and recordings stay in the browser on each device. Nothing is uploaded except the audio you choose to transcribe, which goes straight to AssemblyAI with your own API key. The key is stored only on your device.

Script links carry the script inside the link itself (after the `#`), which browsers never send to the website.

## If AssemblyAI uploads are blocked

Some browsers refuse to send files straight to AssemblyAI. In that case deploy [`relay/worker.js`](relay/worker.js) as a free Cloudflare Worker (instructions at the top of the file) and paste its URL into **Wrap › Advanced › Relay URL**.

## Package format

`session.json` is `cueline-session/2`: `scripts[]`, one take list with `scriptId` per take, `speechStart`/`speechEnd` (where the voice sat inside each take), `auto` (heard but never marked), and `session.gaps[]`. Times are seconds from the start of `audio/full-recording.wav`.

## Script link format

`https://charliefehr09-longheld.github.io/Cueline/#cue1=` followed by base64url of the raw-DEFLATE-compressed JSON `{"t": title, "b": body}`.

## Controls

| Key | Scroll mode | Take mode |
| --- | --- | --- |
| Right / Left | Faster / slower, scrub when paused | Next / previous line |
| Space or Enter | Play / pause | Start / stop a take (hold to mark good). Marks only: press = good |
| G / X | | Mark good / scratch |
| Page Down / Up | Next / previous section, next / previous queued script at the ends | Same |
| [ / ] | Text smaller / larger | Text smaller / larger |
| F | Full screen script (tap for the exit button) | Full screen script |
| M | Mirror | Mirror |
| S / L | | Slate / take log |
