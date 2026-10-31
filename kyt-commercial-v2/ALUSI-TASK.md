# Task for Alusi: render "Know Your Type" commercial v2

Paste the block below to Alusi (Telegram or the OpenClaw chat) on the Mac mini.

```
Task: render the Know Your Type v2 commercial. Scope is limited to this task only.

1. If ~/openclaw-projects/kyt-commercial exists, run `git -C ~/openclaw-projects/kyt-commercial pull`.
   Otherwise run:
   git clone --depth 1 -b claude/kyt-commercial-v2-btxcjx https://github.com/UA4200/antfarm.git ~/openclaw-projects/kyt-commercial
2. cd ~/openclaw-projects/kyt-commercial/kyt-commercial-v2 && ./run_on_mac.sh
   (If it stops with "kyt-narration.mp3 not found", find the file and re-run it as
   ./run_on_mac.sh /full/path/to/kyt-narration.mp3)
3. Send me receipt.txt, qa/sheet.png, and any qa/f_*.png listed on a VIEW line.

Allowed: Homebrew installs of ffmpeg, tesseract, and font-dejavu; Pillow in the folder's .venv.
Not allowed: any other installs, uploading or posting the video, editing the scripts,
deleting anything outside that folder, or touching ~/.openclaw/workspace/antfarm.
If the run fails, stop after 1 retry and send me the last 30 lines of output. Do not improvise fixes.
```

Done means receipt.txt ends with `RESULT: PASS` and I have viewed sheet.png.
