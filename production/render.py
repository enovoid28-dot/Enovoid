#!/usr/bin/env python3
import json, subprocess, shutil, sys, wave, math, struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'; TMP=OUT/'tmp'; OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe()
M=json.loads((ROOT/'production/manifest.json').read_text())

def run(cmd):
    print('+',' '.join(map(str,cmd)), flush=True)
    subprocess.run(list(map(str,cmd)),check=True)

def duration(path):
    p=subprocess.run([FF,'-i',str(path)],capture_output=True,text=True)
    import re
    m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr)
    return int(m[1])*3600+int(m[2])*60+float(m[3]) if m else 0

# Fail closed: render only audited allowlist.
for rel in M['approved_scenes']:
    p=ROOT/rel
    with Image.open(p) as im:
        im.verify()
    with Image.open(p) as im:
        w,h=im.size
        if not 1.70 < w/h < 1.82: raise SystemExit(f'Invalid aspect ratio: {rel} {w}x{h}')

# Join narration without re-encoding so no spoken word is clipped.
concat=TMP/'voice.txt'
concat.write_text(''.join(f"file '{(ROOT/x).as_posix()}'\n" for x in M['voice_tracks']))
voice=TMP/'voice.mp3'
run([FF,'-y','-f','concat','-safe','0','-i',concat,'-c','copy',voice])
voice_d=duration(voice)
if voice_d < M['minimum_duration_seconds']: raise SystemExit(f'Narration too short: {voice_d}')

# Procedural (non-generative-AI) transition effects: short soft sweeps/clicks.
def wav_sfx(path, kind, seconds=.34, sr=48000):
    n=int(seconds*sr)
    with wave.open(str(path),'w') as w:
        w.setparams((1,2,sr,n,'NONE','not compressed'))
        for i in range(n):
            t=i/sr; env=math.sin(math.pi*i/n)**2
            if kind=='whoosh': val=(math.sin(2*math.pi*(180+1500*t*t)*t))*env*.18
            else: val=math.sin(2*math.pi*900*t)*math.exp(-18*t)*.22
            w.writeframesraw(struct.pack('<h',int(max(-1,min(1,val))*32767)))
whoosh=TMP/'whoosh.wav'; click=TMP/'click.wav'; wav_sfx(whoosh,'whoosh'); wav_sfx(click,'click',.18)

# Two visual beats per narration chapter. Tiny padding keeps final spoken syllable intact.
seg=(voice_d+1.2)/len(M['approved_scenes'])
clips=[]
for i,rel in enumerate(M['approved_scenes']):
    clip=TMP/f'scene-{i:02d}.mp4'; clips.append(clip)
    frames=math.ceil(seg*M['fps'])
    # Alternating slow push-in/pull-out plus fade transition.
    z="min(zoom+0.00018,1.07)" if i%2==0 else "if(eq(on,0),1.07,max(zoom-0.00018,1.0))"
    vf=(f"scale=1344:756:force_original_aspect_ratio=increase,crop=1344:756,"
        f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1280x720:fps={M['fps']},"
        f"fade=t=in:st=0:d=0.35,fade=t=out:st={max(0,seg-0.35):.3f}:d=0.35,format=yuv420p")
    run([FF,'-y','-loop','1','-i',ROOT/rel,'-vf',vf,'-t',f'{seg:.3f}','-an',
         '-c:v','libx264','-preset','veryfast','-crf','21','-movflags','+faststart',clip])
video_list=TMP/'video.txt'; video_list.write_text(''.join(f"file '{p.as_posix()}'\n" for p in clips))
silent=TMP/'silent.mp4'
run([FF,'-y','-f','concat','-safe','0','-i',video_list,'-c','copy',silent])

# Overlay transition effects at scene boundaries, kept subtle under narration.
inputs=[FF,'-y','-i',silent,'-i',voice]
for _ in range(9): inputs += ['-i',whoosh]
filters=[]
for j in range(9):
    ms=int(seg*(j+1)*1000)
    filters.append(f'[{j+2}:a]volume=0.34,adelay={ms}|{ms}[s{j}]')
filters.append('[1:a]volume=1.0[n]')
filters.append('[n]'+''.join(f'[s{j}]' for j in range(9))+f'amix=inputs=10:duration=first:normalize=0,alimiter=limit=0.95[a]')
final=OUT/'bukan-malas-prokrastinasi.mp4'
run(inputs+['-filter_complex',';'.join(filters),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',final])

# Thumbnail, derived from approved artwork only.
base=Image.open(ROOT/M['approved_scenes'][0]).convert('RGB')
base=ImageOps.fit(base,(1280,720))
over=Image.new('RGBA',base.size,(0,0,0,0)); d=ImageDraw.Draw(over)
d.rounded_rectangle((45,390,760,655),radius=28,fill=(4,10,22,220),outline=(255,88,69,255),width=8)
font_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
fp=next((x for x in font_paths if Path(x).exists()),None)
f1=ImageFont.truetype(fp,90) if fp else ImageFont.load_default(); f2=ImageFont.truetype(fp,72) if fp else ImageFont.load_default()
d.text((80,410),'BUKAN',font=f1,fill='white',stroke_width=5,stroke_fill='black')
d.text((80,505),'MALAS!',font=f1,fill=(255,88,69),stroke_width=5,stroke_fill='black')
thumb=Image.alpha_composite(base.convert('RGBA'),over).convert('RGB'); thumb.save(OUT/'thumbnail.jpg',quality=94)

# Final verification report.
fd=duration(final)
report={'video':final.name,'duration_seconds':round(fd,2),'resolution':'1280x720','fps':M['fps'],
        'voice_duration_seconds':round(voice_d,2),'approved_scene_count':len(M['approved_scenes']),
        'rejected_scene_count':len(M['rejected_scenes']),'checks_passed':fd>240 and fd>=voice_d-1}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
if not report['checks_passed']: raise SystemExit(f'Final verification failed: {report}')
print(json.dumps(report,indent=2))
