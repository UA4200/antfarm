# Know Your Type — commercial v2 (test project)

Self-contained folder. Deleting it removes everything this work added to the repo.

| File | Purpose |
|---|---|
| `build_commercial.py` | One-pass Pillow → ffmpeg renderer (13 beat-synced cards, 1080x1920, 30fps, 26.5s) |
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
