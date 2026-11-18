#!/usr/bin/env bash
# Render ulang video dari nol: gambar -> video per adegan -> gabung -> audio -> mux.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p output/segments
JOBS=${JOBS:-2}

# 1) daftar adegan (nama, frame awal, frame akhir) dari timeline di scenes.py
python3 - <<'PY' > output/segments/jobs.txt
import sys; sys.path.insert(0, 'src')
from scenes import SCENES
for i, (a, b, fn) in enumerate(SCENES):
    print(f"output/segments/seg{i} {round(a*30)} {round(b*30)}")
PY

# 2) render tiap adegan paralel (cairo -> raw frames -> ffmpeg libx264)
(cd src && sed 's#^output/#../output/#' ../output/segments/jobs.txt | xargs -P "$JOBS" -L 1 python3 render.py)

# 3) gabung adegan tanpa encode ulang
awk '{print "file '\''" substr($1, length("output/segments/")+1) ".mp4'\''"}' output/segments/jobs.txt > output/segments/list.txt
ffmpeg -v error -y -f concat -safe 0 -i output/segments/list.txt -c copy output/video_tanpa_audio.mp4

# 4) audio: musik + SFX prosedural + voiceover, lalu loudness -14 LUFS (standar Instagram)
(cd src && python3 audio.py ../voiceover/voiceover.wav ../output/audio_mix.wav)
ffmpeg -v error -y -i output/audio_mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 output/audio_final.wav

# 5) mux final 9:16 (Reels) + versi 4:5 (feed)
ffmpeg -v error -y -i output/video_tanpa_audio.mp4 -i output/audio_final.wav -map 0:v -map 1:a \
  -c:v libx264 -profile:v high -level 4.1 -preset slow -b:v 8M -maxrate 10M -bufsize 16M -r 30 -pix_fmt yuv420p \
  -c:a aac -b:a 256k -movflags +faststart output/reels_9x16.mp4
ffmpeg -v error -y -i output/reels_9x16.mp4 -vf "crop=1080:1350:0:285" -c:v libx264 -crf 18 -preset veryfast \
  -pix_fmt yuv420p -c:a copy -movflags +faststart output/feed_4x5.mp4
echo "Selesai: output/reels_9x16.mp4 dan output/feed_4x5.mp4"
