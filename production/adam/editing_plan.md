# Editing Plan — Kisah Nabi Adam

## Master settings

- Format: YouTube long-form
- Resolution: 1920x1080
- Aspect ratio: 16:9
- Frame rate: 30 fps recommended
- Audio: 48 kHz stereo
- Master voice-over: `audio/voiceover_full.mp3`
- Measured voice-over duration: approximately 6:47
- Subtitle: `subtitles_id.srt`
- Visuals: `images/generated/scene_01.jpg` through `scene_45.jpg`
- Final image approval: `master_image_audit.md`

## Editing rules

1. Render only scenes 01–45 from the latest approved set.
2. Use the final timecodes in `storyboard.md`, which have been retimed to the measured voice-over.
3. Apply slow zoom, pan, light parallax, or crop only when it supports the narration.
4. Do not use camera movement to hide missing images.
5. Keep subtitle text away from Adam's face glow and other important objects.
6. Add all on-screen emphasis text during editing, never inside generated images.
7. Keep the right side of scene 45 clear for the YouTube end screen.

## Transitions

- Default cut: hard cut or short cross dissolve, 6–10 frames.
- Hook to context: soft fade through dark blue.
- Creation and knowledge: light dissolve.
- Iblis introduction: short directional wipe with restrained dark whoosh.
- Garden sequence: cross dissolve and gentle match cuts.
- Godaan: one restrained blur transition.
- Taubat: warm light dissolve.
- Turun ke bumi: fade through pale light, not a falling effect.
- Ending: slow fade to warm white or dark blue for end screen.

Do not use a transition on every cut. Avoid flashy zoom transitions, glitch effects, and excessive motion.

## Sound design plan

| Bagian | SFX yang sesuai | Level awal yang disarankan |
|---|---|---:|
| Hook and cosmic opening | Soft wind, low airy riser | -24 to -20 dB under VO |
| Earth and creation | Low earth movement, soft whoosh | -24 dB under VO |
| Knowledge | Gentle chime, very low ambience | -26 to -22 dB under VO |
| Iblis | Restrained smoke whoosh, low dark ambience | -26 to -22 dB under VO |
| Garden | Leaves, soft wind, distant water | -28 to -24 dB under VO |
| Temptation | Short low riser, leaves | -28 to -24 dB under VO |
| Repentance | Soft chime, warm airy tone | -30 to -26 dB under VO |
| Earth and guidance | Footsteps, wind, distant ambience | -28 to -24 dB under VO |
| Outro | Soft chime and low wind | -30 to -26 dB under VO |

SFX harus selalu lebih rendah daripada voice-over. Gunakan hanya file berlisensi atau bebas digunakan dan catat URL, pencipta, lisensi, serta tanggal akses di `sfx_sources.md` sebelum publikasi. Tidak ada klaim lisensi SFX yang dibuat sebelum sumbernya dicatat.

## Voice-over mixing

- Gunakan `voiceover_full.mp3` sebagai dialog utama tanpa mempercepat atau memperlambatnya.
- Jangan memotong awal atau akhir kalimat.
- Jangan menormalisasi secara agresif hingga suara terdengar pecah.
- Gunakan ducking pada musik atau SFX setiap kali voice-over berbicara.
- Target akhir loudness dapat disesuaikan di editor, dengan prioritas artikulasi narator dan tanpa clipping.
- Lima file bagian tetap disimpan sebagai backup jika editor perlu memperbaiki satu bagian tanpa membuat ulang seluruh voice-over.
