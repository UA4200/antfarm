#!/usr/bin/env python3
"""Build kyt-narration.mp3 (24.55s) with Piper TTS, one line per beat.

Each line is synthesized separately, trimmed, fitted to its slot, and placed at
its sync-map voice start, so the cards in build_commercial.py stay in sync.

Usage:
    python3 make_narration.py VOICE.onnx [SPEAKER_ID] [out.mp3]

Voice used for v2: Piper "en-us-libritts-high" (LibriTTS dataset, CC BY 4.0,
commercial use allowed with attribution), speaker 660. Do NOT use Piper voices
whose MODEL_CARD license is non-commercial (e.g. ryan: CC BY-NC-SA).
"""
import os
import subprocess
import sys
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = sys.argv[1]
SPEAKER = int(sys.argv[2]) if len(sys.argv) > 2 else 660
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "kyt-narration.mp3")

TOTAL = 24.55
GAP = 0.12            # minimum silence before the next beat
MIN_LENGTH_SCALE = 0.80  # fastest re-synthesis before falling back to atempo

# (voice_start, spoken line) — starts match CARDS in build_commercial.py
BEATS = [
    (0.0, "I liked 300 photos on Instagram."),
    (2.9, "Then I asked AI a dangerous question."),
    (5.5, "What is my type?"),
    (7.1, "It sorted every single like."),
    (9.3, "The faith-first boss."),
    (10.8, "The comedian funnier than me."),
    (12.8, "The millionaire founder."),
    (14.3, "Self-reported types lie."),
    (16.3, "Like history doesn't."),
    (17.8, "It ranked my top ten, and it was right."),
    (20.4, "Know your type."),
    (21.4, "Nine ninety-nine."),
    (22.7, "Your data never leaves your phone."),
]

voice = PiperVoice.load(MODEL)
SR = voice.config.sample_rate


def synth(text, length_scale):
    cfg = SynthesisConfig(speaker_id=SPEAKER, length_scale=length_scale,
                          noise_scale=0.5, noise_w_scale=0.6)
    a = np.concatenate([c.audio_float_array for c in voice.synthesize(text, syn_config=cfg)])
    # Trim leading/trailing silence so the first word lands on the beat start.
    loud = np.flatnonzero(np.abs(a) > 0.02)
    return a[max(0, loud[0] - int(0.01 * SR)): loud[-1] + int(0.05 * SR)]


def atempo(a, factor):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
         "-af", f"atempo={factor:.4f}", "-f", "f32le", "-"],
        input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


track = np.zeros(int(TOTAL * SR), dtype=np.float32)
ends = [b[0] for b in BEATS[1:]] + [TOTAL]
print(f"speaker {SPEAKER} @ {SR}Hz")
for (start, text), end in zip(BEATS, ends):
    slot = end - start - GAP
    ls = 1.0
    clip = synth(text, ls)
    while len(clip) / SR > slot and ls > MIN_LENGTH_SCALE:
        ls = max(MIN_LENGTH_SCALE, ls * slot / (len(clip) / SR))
        clip = synth(text, ls)
    note = f"length_scale={ls:.2f}"
    if len(clip) / SR > slot:
        f = (len(clip) / SR) / slot
        clip = atempo(clip, f)
        note += f" atempo={f:.2f}"
    i = int(round(start * SR))
    track[i:i + len(clip)] += clip[: len(track) - i]
    print(f"{start:5.1f}s  {len(clip)/SR:4.2f}/{slot:4.2f}s  {note:28s} {text}")

peak = np.abs(track).max()
track = track / peak * 0.89  # ~-1 dBFS; loudness is normalized later by the renderer
pcm = (track * 32767).astype(np.int16)
tmp = OUT + ".wav"
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-ar", "44100", "-c:a", "libmp3lame",
                "-b:a", "192k", "-map_metadata", "-1", "-t", str(TOTAL), OUT], check=True)
os.remove(tmp)
print(f"wrote {OUT}")
