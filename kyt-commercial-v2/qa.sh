#!/usr/bin/env bash
# QA for know-your-type-commercial-v2.mp4 (work order v2, checks 1-5 + OCR).
# Usage: ./qa.sh [video.mp4]
set -uo pipefail
cd "$(dirname "$0")"
OUT="${1:-know-your-type-commercial-v2.mp4}"
QA=qa
mkdir -p "$QA"
fail=0

echo "== 1. Streams"
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration -of default=nw=1 "$OUT"
probe=$(ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration -of default=nw=1 "$OUT")
grep -q "width=1080" <<<"$probe" && grep -q "height=1920" <<<"$probe" && grep -q "r_frame_rate=30/1" <<<"$probe" \
  && grep -q "codec_type=audio" <<<"$probe" || { echo "FAIL streams"; fail=1; }
dur=$(sed -n 's/^duration=//p' <<<"$probe" | tail -1)
awk -v d="$dur" 'BEGIN{exit !(d>=26 && d<=27)}' && echo "PASS duration $dur" || { echo "FAIL duration $dur"; fail=1; }

# ocr <time> <expected text> <label>
ocr() {
  local t=$1 want=$2 label=$3 png="$QA/f_$1.png"
  # Frame on screen at time t = floor(t*30). (-ss would return the NEXT frame when t
  # falls between frame starts, which makes start-0.13 land on the new card.)
  local n
  n=$(awk -v t="$t" 'BEGIN{printf "%d", int(t*30+1e-6)}')
  ffmpeg -v error -y -i "$OUT" -vf "select=eq(n\\,$n)" -vsync 0 -frames:v 1 "$png"
  # Crop out the brand mark (top) and caption (bottom); OCR the main text block only.
  local got
  got=$(ffmpeg -v error -y -i "$png" -vf "crop=1080:1080:0:380" -f image2pipe -vcodec png - \
        | tesseract - - --psm 6 2>/dev/null | tr '\n' ' ' | tr -s ' ')
  # Fuzzy match: OCR confuses I/| and similar glyphs. Pass at >=0.8 similarity.
  if python3 -c 'import sys,difflib,re
n=lambda x: re.sub(r"[^a-z0-9$]","",x.lower().replace("|","i"))
g,w=n(sys.argv[1]),n(sys.argv[2])
sys.exit(0 if w in g or difflib.SequenceMatcher(None,g,w).ratio()>=0.8 else 1)' "$got" "$want"; then
    printf 'PASS %-6s %-5s %s\n' "$t" "$label" "$want"
  elif [[ "$want" == '$9.99' ]]; then
    # Work order: "$9.99" OCRs poorly (esp. mid fade-in). Flag for a visual check, don't fail.
    printf 'VIEW %-6s %-5s %s -> open %s\n' "$t" "$label" "$want" "$png"
  else
    printf 'FAIL %-6s %-5s want=%q got=%q\n' "$t" "$label" "$want" "$got"
    return 1
  fi
}

TEXTS=("I liked 300 photos." "Then I asked AI a dangerous question:" "WHAT IS MY TYPE?" \
  "It sorted every single like." "The faith-first boss." "The comedian funnier than me." \
  "The millionaire founder." "Self-reported types lie." "Like history doesn't." \
  "It ranked my top ten, and it was right." "KNOW YOUR TYPE" "\$9.99" \
  "Your data never leaves your phone.")
STARTS=(0.0 2.9 5.5 7.1 9.3 10.8 12.8 14.3 16.3 17.8 20.4 21.4 22.7)

echo "== 2. Content spot checks"
ocr 6.0 "WHAT IS MY TYPE?" c3 || fail=1
ocr 16.7 "Like history doesn't." c9 || fail=1
ocr 23.0 "Your data never leaves your phone." c13 || fail=1

echo "== 3. Boundary check (start-0.13 = previous card, start-0.07 = new card)"
for n in $(seq 1 12); do
  s=${STARTS[$n]}
  before=$(awk -v s="$s" 'BEGIN{printf "%.2f", s-0.13}')
  after=$(awk -v s="$s" 'BEGIN{printf "%.2f", s-0.07}')
  ocr "$before" "${TEXTS[$((n-1))]}" "c$n" || fail=1
  ocr "$after" "${TEXTS[$n]}" "c$((n+1))" || fail=1
done

echo "== 4. Audio silence gaps (-35dB, >=0.3s)"
ffmpeg -hide_banner -i "$OUT" -af silencedetect=noise=-35dB:d=0.3 -f null - 2>&1 | grep -E "silence_(start|end)"

echo "== 5. Metadata"
tags=$(ffprobe -v error -show_entries format_tags:stream_tags -of default=nw=1 "$OUT")
echo "$tags"
if grep -qiE "artist|author|comment|album|composer|copyright" <<<"$tags"; then echo "FAIL metadata"; fail=1; fi
grep -q "TAG:title=Know Your Type" <<<"$tags" && echo "PASS title" || { echo "FAIL title"; fail=1; }

echo "== Frame sheet: $QA/sheet.png"
ffmpeg -v error -y -i "$OUT" -vf "select='eq(n\,30)+eq(n\,120)+eq(n\,180)+eq(n\,240)+eq(n\,300)+eq(n\,345)+eq(n\,396)+eq(n\,450)+eq(n\,501)+eq(n\,555)+eq(n\,618)+eq(n\,654)+eq(n\,690)',scale=270:480,tile=13x1" -frames:v 1 "$QA/sheet.png"

[[ $fail == 0 ]] && echo "QA: ALL PASS" || echo "QA: FAILURES ABOVE"
exit $fail
