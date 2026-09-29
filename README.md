# Enovoid — Animasi Stickman Indonesia

Produksi video YouTube long-form 16:9 berbasis rangkaian gambar stickman, narasi Indonesia, transisi, dan efek suara non-AI.

## Rilis pertama

**Bukan Malas! Alasan Otakmu Suka Menunda (dan Cara Mengatasinya)**

Paket publikasi pada GitHub Release berisi:

- MP4 final 1280×720, 24 fps, durasi 6:43;
- thumbnail JPG 1280×720;
- metadata YouTube lengkap.

## Kontrol kualitas

`production/manifest.json` adalah allowlist adegan. Renderer tidak memindai folder secara otomatis, sehingga gambar gagal atau belum diaudit tidak dapat masuk ke video. `production/render.py` memvalidasi decoding, rasio, durasi minimum, dan keutuhan durasi narasi sebelum menyatakan render lolos.

Efek transisi dibuat secara prosedural (gelombang audio biasa), bukan generative AI. Voice-over dan gambar dibuat khusus untuk proyek ini.

## Reproduksi

```bash
python3 -m pip install pillow imageio-ffmpeg
python3 production/render.py
```

Output dibuat di folder `output/` dan sengaja tidak dilacak Git karena video final didistribusikan lewat GitHub Release.
