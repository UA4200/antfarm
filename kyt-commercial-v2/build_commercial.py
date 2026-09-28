#!/usr/bin/env python3
"""Render know-your-type-commercial-v2.mp4 (1080x1920, 30fps, 26.5s).

Typography-only cards, beat-synced to the existing narration. Pillow draws
each frame; frames are piped to ffmpeg as raw RGB.

Usage:
    python3 build_commercial.py [narration.mp3] [output.mp4]

Defaults: kyt-narration.mp3 / know-your-type-commercial-v2.mp4 next to this file.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
NARRATION = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "kyt-narration.mp3")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "know-your-type-commercial-v2.mp4")

W, H, FPS, TOTAL, LEAD = 1080, 1920, 30, 26.5, 0.10
PUSH_IN, FADE_FRAMES = 0.35, 3
BG, WHITE, DIM = (10, 10, 15), (242, 242, 245), (154, 154, 173)
RED, GOLD = (255, 61, 90), (245, 197, 24)
MAX_W, LINE_H, CENTER_Y = 880, 1.15, 0.45
SAFE_TOP, SAFE_BOTTOM = 220, H - 380

# First match wins: Inter/Montserrat Bold, then DejaVu Sans Bold (spec order).
FONT_CANDIDATES = [
    "/Library/Fonts/Inter-Bold.ttf",
    os.path.expanduser("~/Library/Fonts/Inter-Bold.ttf"),
    "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/Library/Fonts/Montserrat-Bold.ttf",
    os.path.expanduser("~/Library/Fonts/Montserrat-Bold.ttf"),
    "/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/opt/homebrew/share/fonts/dejavu-fonts/DejaVuSans-Bold.ttf",
    "/Library/Fonts/DejaVuSans-Bold.ttf",
    os.path.expanduser("~/Library/Fonts/DejaVuSans-Bold.ttf"),
]

# (voice_start, text, color, size)
CARDS = [
    (0.0, "I liked 300 photos.", WHITE, 88),
    (2.9, "Then I asked AI a dangerous question:", DIM, 72),
    (5.5, "WHAT IS MY TYPE?", RED, 120),
    (7.1, "It sorted every single like.", DIM, 72),
    (9.3, "The faith-first boss.", WHITE, 88),
    (10.8, "The comedian funnier than me.", WHITE, 88),
    (12.8, "The millionaire founder.", WHITE, 88),
    (14.3, "Self-reported types lie.", DIM, 72),
    (16.3, "Like history doesn't.", WHITE, 88),
    (17.8, "It ranked my top ten, and it was right.", WHITE, 88),
    (20.4, "KNOW YOUR TYPE", WHITE, 130),
    (21.4, "$9.99", GOLD, 220),
    (22.7, "Your data never leaves your phone.", WHITE, 88),
]
HERO_CARD = 10  # "KNOW YOUR TYPE": brand mark hidden on this card

# Card cut points on the frame grid. Card 1 starts at 0; others lead the voice by LEAD.
START_FRAMES = [0] + [round((c[0] - LEAD) * FPS) for c in CARDS[1:]] + [round(TOTAL * FPS)]


def die(msg):
    sys.exit(f"STOP: {msg}")


def pick_font():
    for p in FONT_CANDIDATES:
        if os.path.isfile(p):
            return p
    die("no Inter/Montserrat/DejaVu Sans Bold font found; install one and re-run")


def preflight():
    if not os.path.isfile(NARRATION):
        die(f"narration not found: {NARRATION}")
    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", NARRATION]).decode().strip())
    if not 24.5 <= dur <= 24.6:
        die(f"narration duration {dur:.3f}s is outside 24.5-24.6s")
    return dur


FONT_PATH = None
_fonts = {}


def font(size):
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT_PATH, size)
    return _fonts[size]


def wrap(text, f):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and f.getlength(trial) > MAX_W:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def text_layer(text, color, size):
    f = font(size)
    lines = wrap(text, f)
    lh = int(size * LINE_H)
    # Pad so glyph descenders/ascenders are not clipped.
    pad = int(size * 0.3)
    img = Image.new("RGBA", (W, lh * len(lines) + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        d.text(((W - f.getlength(ln)) / 2, pad + i * lh), ln, font=f, fill=color)
    return img.crop(img.getbbox())


def base(i):
    b = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(b)
    if i != HERO_CARD:
        d.text((60, 230), "KNOW YOUR TYPE", font=font(32), fill=DIM)
    if i == 0:
        f = font(30)
        cap = "AI-voiced narration"
        d.text(((W - f.getlength(cap)) / 2, 1500), cap, font=f, fill=DIM)
    return b


def main():
    global FONT_PATH
    dur = preflight()
    FONT_PATH = pick_font()
    print(f"narration {dur:.3f}s | font {FONT_PATH}")

    layers = [text_layer(c[1], c[2], c[3]) for c in CARDS]
    bases = [base(i) for i in range(len(CARDS))]

    # Safe-zone check at full scale (the largest the layer ever gets).
    for (_, text, _, _), lay in zip(CARDS, layers):
        top = H * CENTER_Y - lay.height / 2
        if lay.width > MAX_W or top < SAFE_TOP or top + lay.height > SAFE_BOTTOM:
            die(f"card {text!r} breaks the safe zone ({lay.width}x{lay.height} at y={top:.0f})")

    cmd = [
        "ffmpeg", "-y", "-v", "error", "-stats",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", NARRATION,
        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,apad",
        "-map", "0:v", "-map", "1:a", "-t", str(TOTAL),
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-map_metadata", "-1", "-map_chapters", "-1",
        "-metadata", "title=Know Your Type",
        "-movflags", "+faststart",
        OUT,
    ]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    ci = 0
    for fr in range(START_FRAMES[-1]):
        while fr >= START_FRAMES[ci + 1]:
            ci += 1
        local = fr - START_FRAMES[ci]
        k = min(1.0, (local / FPS) / PUSH_IN)
        s = 0.94 + 0.06 * (1 - (1 - k) ** 3)  # ease-out cubic
        # Cut frame already shows the new card (1/3 opacity), full by frame 3.
        alpha = min(1.0, (local + 1) / FADE_FRAMES)

        lay = layers[ci]
        if s < 1.0:
            lay = lay.resize((round(lay.width * s), round(lay.height * s)), Image.LANCZOS)
        if alpha < 1.0:
            lay = lay.copy()
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
        frame = bases[ci].copy()
        frame.alpha_composite(lay, ((W - lay.width) // 2, round(H * CENTER_Y - lay.height / 2)))
        ff.stdin.write(frame.convert("RGB").tobytes())

    ff.stdin.close()
    if ff.wait() != 0:
        die(f"ffmpeg exited {ff.returncode}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
