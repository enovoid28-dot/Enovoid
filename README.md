# 🎥 Enovoid - Automated YouTube Video Production Engine (Stickman Historical Animation)

Sistem produksi otomatis video cerita animasi stickman beresolusi Full HD (1080p), dilengkapi voice-over Bahasa Indonesia yang tegas dan santai, transisi dinamis, efek kamera sinematik (*Ken Burns Effect*), serta sound effects (SFX) perang mendalam tanpa musik.

---

## 📁 Struktur Repositori

```text
Enovoid/
├── assets/                          # Ilustrasi scene animasi stickman 2D (16:9) & thumbnail
│   ├── scene1_pill_choice.png       # Scene 1: Dilema pil merah vs pil biru
│   ├── scene2_colonial_forces.png   # Scene 2: Pasukan kolonial Sekutu & NICA berbaris
│   ├── scene3_military_hq_planning.png # Scene 3: Rapat taktik markas militer pejuang
│   ├── scene4_city_on_fire.png      # Scene 4: Lautan api kota Bandung & evakuasi
│   ├── scene5_ammo_depot_hero.png   # Scene 5: Peledakan gudang amunisi Dayeuhkolot
│   ├── scene6_ashes_victory.png     # Scene 6: Puing abu kemenangan moral & fajar
│   └── youtube_thumbnail.png        # Thumbnail YouTube resolusi tinggi (High-CTR)
├── audio/                           # Rekaman Voice-Over narasi Bahasa Indonesia (Pria Tegas)
│   ├── narration_01.mp3
│   ├── narration_02.mp3
│   ├── narration_03.mp3
│   ├── narration_04.mp3
│   └── narration_05.mp3
├── sfx/                             # Sound effects pertempuran & transisi
│   ├── whoosh.wav                   # Efek transisi antar adegan
│   ├── dramatic_impact.wav          # Efek penekanan/dentuman dramatis
│   ├── tension_rumble.wav           # Gemuruh tensi atmosfer bunker/kota
│   ├── fire_roaring.wav             # Suara kobaran api & reruntuhan terbakar
│   └── explosion.wav                # Efek ledakan dahsyat gudang mesiu
├── scripts/                         # Script rendering otomatis
│   └── render_video.py              # Engine komposit video, audio SFX & transisi
├── release_assets/                  # File hasil render final siap rilis / download
│   ├── Bandung_Lautan_Api_Stickman_Animation.mp4 # Video YouTube Full HD 1080p
│   └── youtube_thumbnail.png        # Thumbnail resmi video
├── YOUTUBE_METADATA.md              # Riset niche, judul, deskripsi, hashtag, & tag SEO
└── README.md
```

---

## 🚀 Fitur Video & Spesifikasi Teknis

- **Durasi Video**: ~1:45 menit (Kategori Long/Mid Form Storytelling)
- **Resolusi**: 1920x1080 (16:9 Full HD)
- **Frame Rate**: 30 FPS Progressive
- **Audio Codec**: AAC Stereo 320 kbps Master Track
- **Voice-Over**: Narasi maskulin, santai namun tegas dalam Bahasa Indonesia.
- **Sound Design**: Full SFX (*Whoosh, Low Drone, Fire Roar, Explosion, Impact Boom*), 100% tanpa musik latar belakang (bebas klaim hak cipta).
- **Visual**: Animasi pergerakan gambar dinamis (*Smooth Zoom In, Pan Right, Dynamic Shake, Zoom Out*) dengan transisi *crossfade* 0.8 detik tanpa teks/subtitel yang mengganggu visual.

---

## 🛠️ Cara Menjalankan Render Ulang

```bash
# Jalankan engine render
python3 scripts/render_video.py
```

Output video otomatis tersimpan di direktori `release_assets/`.
