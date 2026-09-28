# Know Your Type — commercial v2 (test project)

Self-contained folder. Deleting it removes everything this work added to the repo.

| File | Purpose |
|---|---|
| `build_commercial.py` | One-pass Pillow → ffmpeg renderer (13 beat-synced cards, 1080x1920, 30fps, 26.5s) |
| `make_narration.py` | Builds `kyt-narration.mp3` with Piper TTS, one line per beat, each placed on its sync-map start |
| `run_on_mac.sh` | Mac mini one-shot: check-first installs, finds the narration, renders, runs QA, writes `receipt.txt` |
| `ALUSI-TASK.md` | Copy-paste message to hand the run to Alusi (OpenClaw) |
| `qa.sh` | QA checks 1–5 from the work order, plus Tesseract OCR on all 13 cuts and a frame contact sheet |

## Run on the Mac mini (one command)
```bash
./run_on_mac.sh [/path/to/kyt-narration.mp3]   # auto-searches ~/Downloads, ~/Desktop, ~/Documents, ~/.openclaw/workspace
```

## Run manually
```bash
cd kyt-commercial-v2
cp /path/to/kyt-narration.mp3 .        # must be 24.5–24.6s or the script stops
python3 build_commercial.py            # -> know-your-type-commercial-v2.mp4
./qa.sh                                # exit 0 = all pass; VIEW lines = open that frame
```
Needs ffmpeg, Pillow, and optionally tesseract. Font order: Inter Bold → Montserrat Bold → DejaVu Sans Bold.
On macOS: `brew install ffmpeg tesseract font-dejavu` if Inter/Montserrat aren't installed.

Inputs (`*.mp3`), renders (`*.mp4`), `qa/`, `.venv/`, and `receipt.txt` are git-ignored.

## Narration (v2 voice)
The v2 voice is synthetic: Piper `en-us-libritts-high`, speaker 660, fetched from
https://github.com/rhasspy/piper/releases/tag/v0.0.2 (`voice-en-us-libritts-high.tar.gz`).
```bash
python3 -m pip install piper-tts
python3 make_narration.py /path/to/en-us-libritts-high.onnx 660   # -> kyt-narration.mp3 (24.55s)
```
**License:** the LibriTTS dataset is CC BY 4.0. Commercial use is allowed, but it needs attribution,
e.g. in the post description: "Voice: Piper TTS, trained on LibriTTS (CC BY 4.0)".
Don't swap in a Piper voice whose MODEL_CARD says non-commercial (e.g. `ryan` is CC BY-NC-SA).
The on-screen "AI-voiced narration" caption on card 1 stays.
