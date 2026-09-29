#!/usr/bin/env python3
"""
Accurate duration video renderer with exact VO & scene alignment
"""

import os
import cv2
import numpy as np
import soundfile as sf
import subprocess

FPS = 30
WIDTH = 1920
HEIGHT = 1080
TRANSITION_SEC = 0.8
TRANSITION_FRAMES = int(TRANSITION_SEC * FPS)

vo_files = [
    'audio/narration_01.mp3',
    'audio/narration_02.mp3',
    'audio/narration_03.mp3',
    'audio/narration_04.mp3',
    'audio/narration_05.mp3'
]

vo_durations = [sf.info(f).duration for f in vo_files]
print("VO durations:", vo_durations)

# Allocate exact scene lengths to give narration plenty of breathing room:
# Scene 1 (Pills choice): VO 1 (17.2s) -> 18.2s
# Scene 2 (Allied troops): VO 2 Part 1 -> 9.5s
# Scene 3 (War HQ planning): VO 2 Part 2 -> 10.5s
# Scene 4 (Bandung fire): VO 3 (23.9s) -> 25.0s
# Scene 5 (Ammunition depot): VO 4 (18.6s) -> 19.8s
# Scene 6 (Dawn / victory): VO 5 (20.3s) -> 22.0s

scene_configs = [
    {
        'image': 'assets/scene1_pill_choice.png',
        'duration': vo_durations[0] + 1.2, # 18.4s
        'effect': 'zoom_in',
        'sfx': [('sfx/dramatic_impact.wav', 0.2, 0.7), ('sfx/tension_rumble.wav', 0.0, 0.35)]
    },
    {
        'image': 'assets/scene2_colonial_forces.png',
        'duration': (vo_durations[1] + 1.0) * 0.48, # 9.18s
        'effect': 'pan_right',
        'sfx': [('sfx/whoosh.wav', 0.0, 0.5), ('sfx/tension_rumble.wav', 0.0, 0.35)]
    },
    {
        'image': 'assets/scene3_military_hq_planning.png',
        'duration': (vo_durations[1] + 1.0) * 0.52 + TRANSITION_SEC, # 10.74s
        'effect': 'zoom_in',
        'sfx': [('sfx/whoosh.wav', 0.0, 0.5)]
    },
    {
        'image': 'assets/scene4_city_on_fire.png',
        'duration': vo_durations[2] + 1.2 + TRANSITION_SEC, # 25.89s
        'effect': 'pan_left_zoom',
        'sfx': [('sfx/whoosh.wav', 0.0, 0.5), ('sfx/fire_roaring.wav', 0.5, 0.5), ('sfx/tension_rumble.wav', 0.0, 0.35)]
    },
    {
        'image': 'assets/scene5_ammo_depot_hero.png',
        'duration': vo_durations[3] + 1.2 + TRANSITION_SEC, # 20.63s
        'effect': 'zoom_in_shake',
        'sfx': [('sfx/whoosh.wav', 0.0, 0.5), ('sfx/explosion.wav', 1.0, 0.85), ('sfx/fire_roaring.wav', 1.5, 0.4)]
    },
    {
        'image': 'assets/scene6_ashes_victory.png',
        'duration': vo_durations[4] + 2.5 + TRANSITION_SEC, # 23.59s
        'effect': 'zoom_out',
        'sfx': [('sfx/whoosh.wav', 0.0, 0.5), ('sfx/dramatic_impact.wav', 0.5, 0.6)]
    }
]

# Calculate accurate start times on timeline after accounting for crossfade overlaps
timeline_starts = [0.0]
for i in range(len(scene_configs) - 1):
    timeline_starts.append(timeline_starts[-1] + scene_configs[i]['duration'] - TRANSITION_SEC)

total_timeline_dur = timeline_starts[-1] + scene_configs[-1]['duration']
print(f"Total calculated video duration: {total_timeline_dur:.2f} seconds ({total_timeline_dur/60:.2f} minutes)")

def get_scene_frame(base_img, effect, progress):
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
        zoom = 1.0 + 0.20 * t
        crop_w = int(bw / zoom)
        crop_h = int(bh / zoom)
        cx, cy = bw // 2, bh // 2
        shake_x, shake_y = 0, 0
        if 0.25 < progress < 0.55:
            decay = 1.0 - (progress - 0.25) / 0.30
            shake_x = int(np.sin(progress * 40 * np.pi) * 12 * decay)
            shake_y = int(np.cos(progress * 35 * np.pi) * 10 * decay)
        x1 = max(0, min(bw - crop_w, cx - crop_w // 2 + shake_x))
        y1 = max(0, min(bh - crop_h, cy - crop_h // 2 + shake_y))
        frame_crop = base_img[y1:y1+crop_h, x1:x1+crop_w]
    else:
        frame_crop = base_img
        
    return cv2.resize(frame_crop, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)

# Preload prepared base images
prepared_images = []
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
    prepared_images.append(img)

scene_frames_count = [int(round(sc['duration'] * FPS)) for sc in scene_configs]

# Audio Mixing
sample_rate = 44100
total_samples = int(total_timeline_dur * sample_rate) + sample_rate
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

# Narration start times
vo_starts = [
    0.4,
    timeline_starts[1] + 0.3,
    timeline_starts[3] + 0.3,
    timeline_starts[4] + 0.3,
    timeline_starts[5] + 0.3
]

for vo_path, t_start in zip(vo_files, vo_starts):
    print(f"VO {vo_path} placed at {t_start:.2f}s")
    add_audio_clip(vo_path, t_start, volume=1.0)

for i, sc in enumerate(scene_configs):
    for sfx_path, offset, vol in sc['sfx']:
        sfx_time = max(0.0, timeline_starts[i] + offset)
        add_audio_clip(sfx_path, sfx_time, volume=vol)

max_peak = np.max(np.abs(master_audio))
if max_peak > 0.95:
    master_audio = master_audio / max_peak * 0.95

os.makedirs('build', exist_ok=True)
master_audio_path = 'build/master_audio.wav'
sf.write(master_audio_path, master_audio, sample_rate)
print("Master audio mixed successfully.")

# Video Pipeline
temp_video = 'build/temp_video.mp4'
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
print("Streaming frames to FFmpeg with ultrafast encoder...")
num_scenes = len(scene_configs)

for s_idx in range(num_scenes):
    total_f = scene_frames_count[s_idx]
    base_img = prepared_images[s_idx]
    effect = scene_configs[s_idx]['effect']
    
    body_frames = total_f - (TRANSITION_FRAMES if s_idx < num_scenes - 1 else 0)
    
    for f in range(body_frames):
        prog = f / max(1, total_f - 1)
        frame = get_scene_frame(base_img, effect, prog)
        proc.stdin.write(frame.tobytes())
        
    if s_idx < num_scenes - 1:
        next_base_img = prepared_images[s_idx + 1]
        next_effect = scene_configs[s_idx + 1]['effect']
        next_total_f = scene_frames_count[s_idx + 1]
        
        for k in range(TRANSITION_FRAMES):
            f_cur = body_frames + k
            prog_cur = f_cur / max(1, total_f - 1)
            frame_cur = get_scene_frame(base_img, effect, prog_cur)
            
            f_next = k
            prog_next = f_next / max(1, next_total_f - 1)
            frame_next = get_scene_frame(next_base_img, next_effect, prog_next)
            
            alpha = (k + 1) / (TRANSITION_FRAMES + 1)
            blended = cv2.addWeighted(frame_next, alpha, frame_cur, 1.0 - alpha, 0)
            proc.stdin.write(blended.tobytes())

proc.stdin.close()
proc.wait()
print("Video stream finished!")

# Final muxing
final_output = 'build/Bandung_Lautan_Api_Stickman_Animation.mp4'
cmd_final = [
    "ffmpeg", "-y", "-i", temp_video, "-i", master_audio_path,
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "320k",
    "-shortest", final_output
]
subprocess.run(cmd_final, check=True)

# Copy deliverables
os.makedirs('release_assets', exist_ok=True)
import shutil
shutil.copyfile(final_output, 'release_assets/Bandung_Lautan_Api_Stickman_Animation.mp4')
shutil.copyfile('assets/youtube_thumbnail.png', 'release_assets/youtube_thumbnail.png')

print("SUCCESS: 100% Complete! Video and thumbnail in release_assets/")
