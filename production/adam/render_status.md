# Render Status

Status: **Asset package ready; MP4 render pending encoder availability**

## Ready

- 45 final images in `images/final/`, each 1920x1080 exact 16:9.
- Voice-over verified and stored in `audio/voiceover_full.mp3`.
- Subtitle timing matches the 406.728 second voice-over.
- Render manifest and concat list are ready.
- Render command is available in `render_video.sh`.

## Pending

The sandbox does not currently contain an MP4 encoder. The render script was tested and stopped cleanly with a clear `ffmpeg is required` message. No fake or silent MP4 was created.

To render the final video in an environment with FFmpeg installed:

```bash
cd production/adam
./render_video.sh
```

Expected output:

```text
final/kisah_nabi_adam_16x9.mp4
```

The command uses the verified voice-over, final exact-16:9 images, H.264 video, AAC audio, and `-shortest` so the video ends with the voice-over rather than cutting it prematurely.
