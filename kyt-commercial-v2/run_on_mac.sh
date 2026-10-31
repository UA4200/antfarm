#!/usr/bin/env bash
# One-shot setup + render + QA for the Know Your Type v2 commercial on the Mac mini.
# Check-first and idempotent: skips anything already present. Safe to re-run.
#
# Usage: ./run_on_mac.sh [/path/to/kyt-narration.mp3]
# Output: know-your-type-commercial-v2.mp4, qa/sheet.png, receipt.txt (all in this folder)
#
# Scope limits (for Alusi): installs only ffmpeg, tesseract, font-dejavu (Homebrew) and
# Pillow (into a local .venv). No other installs, no uploads, no posting, no deletes
# outside this folder.
set -euo pipefail
cd "$(dirname "$0")"
HERE=$(pwd)
say() { printf '\n== %s\n' "$*"; }
stop() { printf '\nSTOP: %s\n' "$*" | tee -a receipt.txt; exit 1; }
: > receipt.txt

say "1. Preflight"
[[ "$(uname)" == Darwin ]] || echo "warning: not macOS; continuing"
command -v brew >/dev/null || stop "Homebrew not found. Install from https://brew.sh then re-run."
for pkg in ffmpeg tesseract; do
  if command -v "$pkg" >/dev/null; then echo "ok  $pkg"; else echo "installing $pkg"; brew install "$pkg"; fi
done
FONT_OK=0
for f in /Library/Fonts/Inter-Bold.ttf ~/Library/Fonts/Inter-Bold.ttf /Library/Fonts/Montserrat-Bold.ttf \
         ~/Library/Fonts/Montserrat-Bold.ttf /Library/Fonts/DejaVuSans-Bold.ttf ~/Library/Fonts/DejaVuSans-Bold.ttf \
         /opt/homebrew/share/fonts/dejavu-fonts/DejaVuSans-Bold.ttf; do
  [[ -f "$f" ]] && { echo "ok  font $f"; FONT_OK=1; break; }
done
[[ $FONT_OK == 1 ]] || { echo "installing font-dejavu"; brew install --cask font-dejavu; }
if [[ ! -x .venv/bin/python ]]; then python3 -m venv .venv; fi
.venv/bin/python -c "import PIL" 2>/dev/null || .venv/bin/python -m pip install -q pillow
echo "ok  Pillow $(.venv/bin/python -c 'import PIL;print(PIL.__version__)')"

say "2. Locate narration"
MP3="${1:-}"
if [[ -z "$MP3" ]]; then
  for d in "$HERE" ~/Downloads ~/Desktop ~/Documents ~/.openclaw/workspace ~/openclaw-projects; do
    [[ -d "$d" ]] || continue
    MP3=$(find "$d" -maxdepth 4 -name kyt-narration.mp3 -print -quit 2>/dev/null || true)
    [[ -n "$MP3" ]] && break
  done
fi
[[ -n "$MP3" && -f "$MP3" ]] || stop "kyt-narration.mp3 not found. Re-run with its path: ./run_on_mac.sh /path/to/kyt-narration.mp3"
[[ "$(cd "$(dirname "$MP3")" && pwd)/$(basename "$MP3")" == "$HERE/kyt-narration.mp3" ]] || cp "$MP3" kyt-narration.mp3
echo "ok  narration $MP3 ($(ffprobe -v error -show_entries format=duration -of csv=p=0 kyt-narration.mp3)s)"

say "3. Render"
.venv/bin/python build_commercial.py 2>&1 | grep -v '^frame=' | tee -a receipt.txt

say "4. QA"
set +e
mkdir -p qa
PATH="$HERE/.venv/bin:$PATH" ./qa.sh 2>&1 | grep -vE '^frame=' > qa/qa.log
QA_RC=${PIPESTATUS[0]}
set -e
grep -E '^(PASS|FAIL|VIEW|QA)|silence_(start|end)|TAG:' qa/qa.log | sed 's/.*\] //' | tee -a receipt.txt

say "5. Receipt"
{
  echo "---"
  echo "date:      $(date -u +%FT%TZ)"
  echo "host:      $(scutil --get ComputerName 2>/dev/null || hostname)"
  echo "git:       $(git -C "$HERE" rev-parse --abbrev-ref HEAD 2>/dev/null) @ $(git -C "$HERE" rev-parse --short HEAD 2>/dev/null)"
  echo "output:    $HERE/know-your-type-commercial-v2.mp4"
  echo "sha256:    $(shasum -a 256 know-your-type-commercial-v2.mp4 | cut -d' ' -f1)"
  echo "qa_exit:   $QA_RC"
  echo "view:      $HERE/qa/sheet.png (and any VIEW frames above)"
} | tee -a receipt.txt
[[ $QA_RC == 0 ]] && echo "RESULT: PASS" | tee -a receipt.txt || echo "RESULT: QA FAILURES — see receipt.txt" | tee -a receipt.txt
exit $QA_RC
