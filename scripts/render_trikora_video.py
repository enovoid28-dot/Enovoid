#!/usr/bin/env python3
"""
Production Engine for Long-Form YouTube Historical Animation:
OPERASI TRIKORA & PERTEMPURAN LAUT ARU (Channel: Stickman Berdasi)

Features:
- Full HD 1080p (1920x1080 @ 30 FPS)
- Duration >= 5.0 Minutes (~5.3 minutes / 320+ seconds)
- 10 Scene Acts with 1:1 Precision Narration Sync
- Dynamic Ken Burns Motion (Pan, Zoom In, Zoom Out, Action Shake)
- Smooth Crossfade Transitions (0.8s)
- Host Presenter Stickman Character Overlay ("Stickman Berdasi" in Sunglasses & Tie)
- Rich Naval War Sound Effects & Transitions (NO BGM Music)
- Clean Visual Storytelling (No Subtitles)
"""

import os
import cv2
import numpy as np
import soundfile as sf
import subprocess
from PIL import Image

FPS = 30
WIDTH = 1920
HEIGHT = 1080
TRANSITION_SEC = 0.8
TRANSITION_FRAMES = int(TRANSITION_SEC * FPS)

vo_files = [f'audio/trikora_vo_{i:02d}.mp3' for i in range(1, 11)]
vo_durations = [sf.info(f).duration for f in vo_files]
print("VO Durations (sec):", [round(d, 2) for d in vo_durations])
print(f"Total pure speech: {sum(vo_durations):.2f}s ({sum(vo_durations)/60:.2f} mins)")

# Scene configurations precisely tailored to narration beats and visual pacing
scene_configs = [
    {
        'id': 1,
        'image': 'assets/trikora_scene01_intro_studio.png',
        'duration': vo_durations[0] + 1.2, # ~32.5s
        'effect': 'zoom_in',
        'host': {'sprite': 'assets/host_explain.png', 'pos': 'bottom_right', 'scale': 0.52},
        'sfx': [
            ('sfx/dramatic_impact.wav', 0.2, 0.75),
            ('sfx/tension_rumble.wav', 0.0, 0.35)
        ]
    },
    {
        'id': 2,
        'image': 'assets/trikora_scene02_bung_karno_trikora.png',
        'duration': vo_durations[1] + 1.0, # ~37.6s
        'effect': 'pan_left_zoom',
        'host': None,
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/dramatic_impact.wav', 2.0, 0.6),
            ('sfx/tension_rumble.wav', 5.0, 0.3)
        ]
    },
    {
        'id': 3,
        'image': 'assets/trikora_scene03_naval_hq_planning.png',
        'duration': vo_durations[2] + 1.0, # ~34.0s
        'effect': 'zoom_in',
        'host': {'sprite': 'assets/host_point.png', 'pos': 'bottom_left', 'scale': 0.48},
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/sonar_ping.wav', 1.5, 0.5),
            ('sfx/tension_rumble.wav', 0.0, 0.35)
        ]
    },
    {
        'id': 4,
        'image': 'assets/trikora_scene04_night_convoy_flare.png',
        'duration': vo_durations[3] + 1.2, # ~32.6s
        'effect': 'pan_right',
        'host': None,
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/flare_launch.wav', 16.0, 0.8),
            ('sfx/tension_rumble.wav', 0.0, 0.4)
        ]
    },
    {
        'id': 5,
        'image': 'assets/trikora_scene05_dutch_destroyers.png',
        'duration': vo_durations[4] + 1.0, # ~28.8s
        'effect': 'zoom_in',
        'host': None,
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/naval_cannon.wav', 2.0, 0.75),
            ('sfx/tension_rumble.wav', 0.0, 0.4)
        ]
    },
    {
        'id': 6,
        'image': 'assets/trikora_scene06_macan_tutul_maneuver.png',
        'duration': vo_durations[5] + 1.0, # ~28.6s
        'effect': 'zoom_in_shake',
        'host': {'sprite': 'assets/host_salute.png', 'pos': 'bottom_right', 'scale': 0.48},
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/naval_cannon.wav', 4.0, 0.85),
            ('sfx/naval_cannon.wav', 14.0, 0.85)
        ]
    },
    {
        'id': 7,
        'image': 'assets/trikora_scene07_yos_sudarso_sacrifice.png',
        'duration': vo_durations[6] + 1.5, # ~28.9s
        'effect': 'zoom_in_shake',
        'host': None,
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/explosion.wav', 1.0, 0.95),
            ('sfx/dramatic_impact.wav', 12.0, 0.7),
            ('sfx/tension_rumble.wav', 15.0, 0.4)
        ]
    },
    {
        'id': 8,
        'image': 'assets/trikora_scene08_submarine_tu16_buildup.png',
        'duration': vo_durations[7] + 1.2, # ~30.8s
        'effect': 'pan_left_zoom',
        'host': {'sprite': 'assets/host_point.png', 'pos': 'bottom_left', 'scale': 0.48},
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/sonar_ping.wav', 3.0, 0.6),
            ('sfx/dramatic_impact.wav', 8.0, 0.7),
            ('sfx/tension_rumble.wav', 0.0, 0.35)
        ]
    },
    {
        'id': 9,
        'image': 'assets/trikora_scene09_papua_victory_un.png',
        'duration': vo_durations[8] + 1.2, # ~26.2s
        'effect': 'zoom_out',
        'host': None,
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/dramatic_impact.wav', 1.5, 0.6)
        ]
    },
    {
        'id': 10,
        'image': 'assets/trikora_scene10_outro_stickman_berdasi.png',
        'duration': vo_durations[9] + 2.5, # ~31.7s
        'effect': 'zoom_in',
        'host': {'sprite': 'assets/host_thumbsup.png', 'pos': 'bottom_right', 'scale': 0.54},
        'sfx': [
            ('sfx/whoosh.wav', 0.0, 0.5),
            ('sfx/dramatic_impact.wav', 0.8, 0.7)
        ]
    }
]

# Calculate timeline start offsets accounting for 0.8s transition crossfades
timeline_starts = [0.0]
for i in range(len(scene_configs) - 1):
    timeline_starts.append(timeline_starts[-1] + scene_configs[i]['duration'] - TRANSITION_SEC)

total_timeline_sec = timeline_starts[-1] + scene_configs[-1]['duration']
print(f"\n==========================================")
print(f"TOTAL CALCULATED VIDEO DURATION: {total_timeline_sec:.2f}s ({total_timeline_sec/60:.2f} minutes)")
print(f"Meets >= 5.0 Minutes requirement: {total_timeline_sec >= 300.0}")
print(f"==========================================\n")

# Load and prepare base scene images (16:9 crop & high quality upscale)
prepared_scene_imgs = []
for sc in scene_configs:
    img = cv2.imread(sc['image'])
    sh, sw = img.shape[:2]
    target_aspect = WIDTH / HEIGHT
    if sw / sh > target_aspect:
        nw = int(sh * target_aspect)
        off = (sw - nw) // 2
        img = img[:, off:off+nw]
    else:
        nh = int(sw / target_aspect)
        off = (sh - nh) // 2
        img = img[off:off+nh, :]
    img = cv2.resize(img, (WIDTH * 4 // 3, HEIGHT * 4 // 3), interpolation=cv2.INTER_AREA)
    prepared_scene_imgs.append(img)

# Load host sprites as RGBA
host_sprites = {}
for spr_name in ['assets/host_explain.png', 'assets/host_point.png', 'assets/host_salute.png', 'assets/host_thumbsup.png']:
    im = Image.open(spr_name).convert('RGBA')
    host_sprites[spr_name] = im

def overlay_host_character(frame_bgr, host_cfg, progress):
    if not host_cfg:
        return frame_bgr
        
    spr_path = host_cfg['sprite']
    pos = host_cfg['pos']
    scale = host_cfg['scale']
    
    sprite = host_sprites[spr_path]
    orig_w, orig_h = sprite.size
    
    target_h = int(HEIGHT * scale)
    target_w = int(orig_w * (target_h / orig_h))
    
    # Slight dynamic breathing / subtle hover float
    hover_y = int(np.sin(progress * 4 * np.pi) * 6)
    
    resized_sprite = sprite.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    if pos == 'bottom_right':
        x = WIDTH - target_w - 40
        y = HEIGHT - target_h + hover_y + 10
    elif pos == 'bottom_left':
        x = 40
        y = HEIGHT - target_h + hover_y + 10
    else:
        x = WIDTH // 2 - target_w // 2
        y = HEIGHT - target_h + hover_y
        
    # Convert OpenCV BGR frame to PIL RGBA
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    pil_frame = Image.fromarray(frame_rgb).convert('RGBA')
    
    # Paste transparent sprite
    pil_frame.paste(resized_sprite, (x, y), resized_sprite)
    
    # Convert back to BGR
    result_bgr = cv2.cvtColor(np.array(pil_frame.convert('RGB')), cv2.COLOR_RGB2BGR)
    return result_bgr

def get_scene_frame(base_img, effect, progress, host_cfg=None):
    bw, bh = base_img.shape[1], base_img.shape[0]
    t = (1 - np.cos(progress * np.pi)) / 2.0
    
    if effect == 'zoom_in':
        zoom = 1.0 + 0.16 * t
        crop_w = int(bw / zoom)
        crop_h = int(bh / zoom)
        cx, cy = bw // 2, bh // 2
        x1 = cx - crop_w // 2
        y1 = cy - crop_h // 2
        frame_crop = base_img[y1:y1+crop_h, x1:x1+crop_w]
    elif effect == 'zoom_out':
        zoom = 1.16 - 0.16 * t
        crop_w = int(bw / zoom)
        crop_h = int(bh / zoom)
        cx, cy = bw // 2, bh // 2
        x1 = cx - crop_w // 2
        y1 = cy - crop_h // 2
        frame_crop = base_img[y1:y1+crop_h, x1:x1+crop_w]
    elif effect == 'pan_right':
        zoom = 1.14
        crop_w = int(bw / zoom)
        crop_h = int(bh / zoom)
        max_offset = bw - crop_w
        x1 = int(max_offset * 0.1 + (max_offset * 0.8) * t)
        y1 = (bh - crop_h) // 2
        frame_crop = base_img[y1:y1+crop_h, x1:x1+crop_w]
    elif effect == 'pan_left_zoom':
        zoom = 1.08 + 0.10 * t
        crop_w = int(bw / zoom)
        crop_h = int(bh / zoom)
        max_offset = bw - crop_w
        x1 = int(max_offset * 0.85 - (max_offset * 0.7) * t)
        y1 = (bh - crop_h) // 2
        frame_crop = base_img[y1:y1+crop_h, x1:x1+crop_w]
    elif effect == 'zoom_in_shake':
        zoom = 1.0 + 0.18 * t
        crop_w = int(bw / zoom)
        crop_h = int(bh / zoom)
        cx, cy = bw // 2, bh // 2
        shake_x, shake_y = 0, 0
        if 0.20 < progress < 0.60:
            decay = 1.0 - (progress - 0.20) / 0.40
            shake_x = int(np.sin(progress * 35 * np.pi) * 14 * decay)
            shake_y = int(np.cos(progress * 30 * np.pi) * 10 * decay)
        x1 = max(0, min(bw - crop_w, cx - crop_w // 2 + shake_x))
        y1 = max(0, min(bh - crop_h, cy - crop_h // 2 + shake_y))
        frame_crop = base_img[y1:y1+crop_h, x1:x1+crop_w]
    else:
        frame_crop = base_img
        
    frame_scaled = cv2.resize(frame_crop, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)
    
    if host_cfg:
        frame_scaled = overlay_host_character(frame_scaled, host_cfg, progress)
        
    return frame_scaled

# Calculate frame counts per scene
scene_frames_count = [int(round(sc['duration'] * FPS)) for sc in scene_configs]

# Mix Master Audio Track
print("\nMixing Master Sound Design & Narration Track...")
sample_rate = 44100
total_samples = int(total_timeline_sec * sample_rate) + sample_rate * 2
master_audio = np.zeros((total_samples, 2), dtype=np.float32)

def add_audio_clip(clip_path, start_time_sec, volume=1.0):
    data, sr = sf.read(clip_path)
    if sr != sample_rate:
        import scipy.signal
        num_new_samples = int(len(data) * sample_rate / sr)
        if data.ndim == 1:
            data = scipy.signal.resample(data, num_new_samples)
        else:
            data = scipy.signal.resample(data, num_new_samples, axis=0)
    
    if data.ndim == 1:
        stereo_clip = np.column_stack([data, data])
    else:
        stereo_clip = data[:, :2]
        
    start_sample = int(start_time_sec * sample_rate)
    clip_len = len(stereo_clip)
    end_sample = min(total_samples, start_sample + clip_len)
    insert_len = end_sample - start_sample
    if insert_len > 0:
        master_audio[start_sample:end_sample] += stereo_clip[:insert_len] * volume

# Place Voice-Overs with 0.3s breath-in offset after each scene starts
for i, vo_path in enumerate(vo_files):
    t_start = timeline_starts[i] + 0.35
    print(f"VO Scene {i+1:02d} ({vo_path}) placed at {t_start:.2f}s")
    add_audio_clip(vo_path, t_start, volume=1.0)

# Place Sound Effects on Timeline
for i, sc in enumerate(scene_configs):
    for sfx_path, offset, vol in sc['sfx']:
        sfx_time = max(0.0, timeline_starts[i] + offset)
        add_audio_clip(sfx_path, sfx_time, volume=vol)

# Master Normalizer
max_peak = np.max(np.abs(master_audio))
if max_peak > 0.95:
    master_audio = master_audio / max_peak * 0.95

os.makedirs('build', exist_ok=True)
master_audio_path = 'build/trikora_master_audio.wav'
sf.write(master_audio_path, master_audio, sample_rate)
print(f"Master audio track exported to {master_audio_path}")

# Stream Render Video Pipeline to FFmpeg
temp_video = 'build/trikora_temp_video.mp4'
ffmpeg_cmd = [
    'ffmpeg', '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', f'{WIDTH}x{HEIGHT}',
    '-pix_fmt', 'bgr24',
    '-r', str(FPS),
    '-i', '-',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-crf', '19',
    '-pix_fmt', 'yuv420p',
    temp_video
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
print("Rendering video frames and streaming to FFmpeg...")

num_scenes = len(scene_configs)

for s_idx in range(num_scenes):
    total_f = scene_frames_count[s_idx]
    base_img = prepared_scene_imgs[s_idx]
    effect = scene_configs[s_idx]['effect']
    host_cfg = scene_configs[s_idx]['host']
    
    body_frames = total_f - (TRANSITION_FRAMES if s_idx < num_scenes - 1 else 0)
    
    for f in range(body_frames):
        prog = f / max(1, total_f - 1)
        frame = get_scene_frame(base_img, effect, prog, host_cfg)
        proc.stdin.write(frame.tobytes())
        
    if s_idx < num_scenes - 1:
        next_base_img = prepared_scene_imgs[s_idx + 1]
        next_effect = scene_configs[s_idx + 1]['effect']
        next_host_cfg = scene_configs[s_idx + 1]['host']
        next_total_f = scene_frames_count[s_idx + 1]
        
        for k in range(TRANSITION_FRAMES):
            f_cur = body_frames + k
            prog_cur = f_cur / max(1, total_f - 1)
            frame_cur = get_scene_frame(base_img, effect, prog_cur, host_cfg)
            
            f_next = k
            prog_next = f_next / max(1, next_total_f - 1)
            frame_next = get_scene_frame(next_base_img, next_effect, prog_next, next_host_cfg)
            
            alpha = (k + 1) / (TRANSITION_FRAMES + 1)
            blended = cv2.addWeighted(frame_next, alpha, frame_cur, 1.0 - alpha, 0)
            proc.stdin.write(blended.tobytes())

proc.stdin.close()
proc.wait()
print("Raw video rendering completed!")

# Multiplex final video & audio
final_output = 'release_assets/Operasi_Trikora_Laut_Aru_Stickman_Berdasi.mp4'
os.makedirs('release_assets', exist_ok=True)

cmd_final = [
    "ffmpeg", "-y", "-i", temp_video, "-i", master_audio_path,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "320k",
    "-shortest", final_output
]
print("Encoding final Master YouTube MP4 video...")
subprocess.run(cmd_final, check=True)

# Copy thumbnail to release assets
import shutil
shutil.copyfile('assets/trikora_youtube_thumbnail.png', 'release_assets/youtube_thumbnail.png')

print(f"\n==========================================")
print(f"SUCCESS: Master Video & Thumbnail exported to release_assets/")
print(f"File: {final_output}")
print(f"==========================================\n")
