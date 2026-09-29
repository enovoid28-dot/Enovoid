#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required to render the final MP4." >&2
  echo "All assets and the exact render manifest are ready in this folder." >&2
  exit 127
fi
mkdir -p final
ffmpeg -y -f concat -safe 0 -i render_concat.txt \
  -i audio/voiceover_full.mp3 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
  -r 30 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart \
  final/kisah_nabi_adam_16x9.mp4
