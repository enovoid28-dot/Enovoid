# 🎬 Stickman Berdasi - Automated YouTube Historical Animation Production Engine

Repositori produksi otomatis video animasi cerita sejarah dan taktik militer bergaya 2D Stickman (*Stickman Berdasi*), berdurasi $\ge 5$ menit (Full HD 1080p), dilengkapi narasi Voice-Over komandan perang Bahasa Indonesia, sound effects (SFX) pertempuran laut, transisi *smooth crossfade*, serta karakter presenter *Stickman Berdasi* berkacamata hitam dan berdasi merah.

---

## 📁 Struktur Repositori

```text
Enovoid/
├── assets/                                     # Gambar adegan stik figur 2D (16:9), sprite presenter & thumbnail
│   ├── trikora_scene01_intro_studio.png        # Scene 1: Studio briefing Stickman Berdasi
│   ├── trikora_scene02_bung_karno_trikora.png  # Scene 2: Pidato Trikora Bung Karno di Yogyakarta
│   ├── trikora_scene03_naval_hq_planning.png   # Scene 3: Perencanaan operasi 4 kapal cepat torpedo
│   ├── trikora_scene04_night_convoy_flare.png  # Scene 4: Konvoi malam disinari suar pesawat Neptune
│   ├── trikora_scene05_dutch_destroyers.png    # Scene 5: Pengepungan kapal perusak Evertsen & Kortenaer
│   ├── trikora_scene06_macan_tutul_maneuver.png# Scene 6: Manuver tajam KRI Macan Tutul memancing tembakan
│   ├── trikora_scene07_yos_sudarso_sacrifice.png# Scene 7: Pengorbanan Yos Sudarso & kobaran api kapal
│   ├── trikora_scene08_submarine_tu16_buildup.png# Scene 8: Armada 12 kapal selam Whiskey & bomber Tu-16
│   ├── trikora_scene09_papua_victory_un.png    # Scene 9: Kemenangan diplomasi & bendera Merah Putih di Papua
│   ├── trikora_scene10_outro_stickman_berdasi.png# Scene 10: Outro studio & tombol subscribe
│   ├── host_explain.png                        # Sprite presenter: Pose menjelaskan
│   ├── host_point.png                          # Sprite presenter: Pose menunjuk
│   ├── host_salute.png                         # Sprite presenter: Pose hormat militer
│   ├── host_thumbsup.png                       # Sprite presenter: Pose jempol / outro
│   └── trikora_youtube_thumbnail.png           # Thumbnail YouTube 1080p (High-CTR)
├── audio/                                      # Master Voice-Over narasi komandan perang Bahasa Indonesia
│   ├── trikora_vo_01.mp3                       # VO Scene 1
│   ├── trikora_vo_02.mp3                       # VO Scene 2
│   ├── trikora_vo_03.mp3                       # VO Scene 3
│   ├── trikora_vo_04.mp3                       # VO Scene 4
│   ├── trikora_vo_05.mp3                       # VO Scene 5
│   ├── trikora_vo_06.mp3                       # VO Scene 6
│   ├── trikora_vo_07.mp3                       # VO Scene 7
│   ├── trikora_vo_08.mp3                       # VO Scene 8
│   ├── trikora_vo_09.mp3                       # VO Scene 9
│   └── trikora_vo_10.mp3                       # VO Scene 10
├── sfx/                                        # Sound effects pertempuran laut
│   ├── whoosh.wav                              # Efek transisi antar adegan
│   ├── dramatic_impact.wav                     # Dentuman sub-bass dramatis
│   ├── naval_cannon.wav                        # Tembakan meriam kapal perusak
│   ├── flare_launch.wav                        # Peluncuran suar & desis cahaya
│   ├── explosion.wav                           # Ledakan kapal & gelombang kejut
│   ├── sonar_ping.wav                          # Sonar kapal selam
│   └── tension_rumble.wav                      # Suara ombak laut malam & tensi
├── scripts/
│   └── render_trikora_video.py                 # Engine rendering video, audio SFX, overlay & transisi
├── release_assets/
│   ├── Operasi_Trikora_Laut_Aru_Stickman_Berdasi.mp4 # File Video Final 1080p (5:06 menit)
│   └── youtube_thumbnail.png                   # Thumbnail resmi YouTube
├── YOUTUBE_METADATA.md                         # Riset keyword, judul A/B, deskripsi SEO, hashtags & tags
└── README.md
```

---

## 🚀 Spesifikasi Teknis Video

- **Judul Proyek**: Operasi Trikora & Pertempuran Laut Aru 1962
- **Channel**: Stickman Berdasi
- **Durasi Video**: **5 Menit 6 Detik (306.37 detik)** $\ge 5$ Menit
- **Resolusi**: 1920x1080 (16:9 Full HD)
- **Frame Rate**: 30 FPS Progressive
- **Audio Codec**: AAC Stereo 320 kbps Master Track
- **Voice-Over**: Suara komandan perang Bahasa Indonesia, tegas dan lugas.
- **Presenter Karakter**: Karakter stickman berkacamata hitam dan berdasi (*Stickman Berdasi*) di sudut bawah layar secara dinamis tanpa menghalangi aksi cerita.
- **Sound Design**: Full SFX (*Naval cannons, sonar, flares, explosions, sub impacts, whooshes*), 100% tanpa musik latar.
- **Visual**: Gerakan kamera dinamis (*Ken Burns: smooth pan, zoom in, zoom out, dynamic shake*) dan transisi *smooth crossfade* 0.8 detik. Bebas subtitel di layar.

---

## 🛠️ Cara Menjalankan Render Ulang

```bash
# Render video lengkap
python3 scripts/render_trikora_video.py
```
