"""Renderer derived from the user-approved Shorts 06–10. No source selection here."""
from pathlib import Path
from tooling import resolve_tool
import subprocess
from PIL import Image, ImageDraw, ImageFont

def run(ff, args, log):
    with Path(log).open('w', encoding='utf8') as stream:
        result = subprocess.run([str(ff), '-y', '-hide_banner', '-loglevel', 'warning', *args], stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(Path(log).read_text(encoding='utf8')[-6000:])

def artwork(plan, edit, folder):
    im = Image.new('RGBA', (1080, 1920)); draw = ImageDraw.Draw(im)
    for y in range(240):
        draw.line((0,y,1080,y), fill=(5,8,13,int(205*(1-y/300))))
    for y in range(1680,1920):
        draw.line((0,y,1080,y), fill=(5,8,13,min(220,int(130+(y-1680)*.4))))
    def center(text, y, size, color):
        font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', size)
        while draw.textbbox((0,0), text, font=font)[2] > 950 and size > 12:
            size -= 1; font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', size)
        box = draw.textbbox((0,0), text, font=font)
        draw.text(((1080-box[2])/2,y), text, font=font, fill=color)
    center(plan['channel'],48,31,'#DAFF64'); center(edit['title'],111,53,'white')
    draw.rounded_rectangle((458,193,622,198),radius=2,fill=edit['color'])
    center(edit['tag'],1711,35,'white'); center(plan['game']+'  /  PHONK',1771,25,edit['color'])
    dest=folder/(edit['name']+'.png'); im.save(dest); return dest

def render(root, plan, edit, encoder='h264_nvenc'):
    if 'music' in edit:plan={**plan,'music':edit['music']}
    if 'game' in edit:plan={**plan,'game':edit['game']}
    ff=resolve_tool('ffmpeg', root); out=root/plan['output']; temp=out/'projeto/render';temp.mkdir(parents=True,exist_ok=True)
    dest=out/(edit['name']+'.mp4')
    if dest.exists(): raise ValueError(f'Arquivo final já existe: {dest}')
    def codec(final=False):
        if encoder=='libx264': return ['-c:v','libx264','-preset','medium','-crf','18' if final else '19']
        return ['-c:v','h264_nvenc','-preset','p5' if final else 'p4','-rc','vbr','-cq','18' if final else '19','-b:v','0']
    parts=[]
    for index,c in enumerate(edit['cuts']):
        length=c['duration'];speed=c['speed'];w=c['width'];h=c['height']
        # Fit a 3:4 crop inside arbitrary source geometry, without stretching narrow footage.
        ch=min(h,int(w*4/3))//2*2;cw=int(ch*.75)//2*2;cy=(h-ch)//2//2*2
        cx=max(0,min(w-cw,int(w*c['center_x']-cw/2)))//2*2
        part=temp/f'{edit["name"]}_{index:02}.mkv';parts.append((part,length))
        vf=f'[0:v]setpts=(PTS-STARTPTS)/{speed},fps=60,split=2[bg][fg];[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,gblur=sigma=16,eq=brightness=-0.11:saturation=0.65,scale=1080:1920[back];[fg]crop={cw}:{ch}:{cx}:{cy},scale=1080:1440:flags=lanczos,eq=contrast=1.04:brightness=0.006:gamma={c["gamma"]}:saturation=1.02[front];[back][front]overlay=0:240,setsar=1[v]'
        af=f'[0:a]asetpts=PTS-STARTPTS,atempo={speed},aresample=48000,apad,atrim=duration={length:.9f},afade=t=in:d=0.007,afade=t=out:st={max(0,length-.01):.9f}:d=0.01[a]'
        run(ff,['-ss',str(c['start']),'-t',str(length*speed+.1),'-i',str(root/c['file']),'-filter_complex_threads','2','-filter_complex',vf+';'+af,'-map','[v]','-map','[a]','-t',f'{length:.9f}','-frames:v',str(c['frames']),*codec(),'-pix_fmt','yuv420p','-c:a','pcm_s16le',str(part)],temp/f'{edit["name"]}_{index:02}.log')
        print(f'{edit["name"]}: corte {index+1}/{len(edit["cuts"])}',flush=True)
    listing=temp/(edit['name']+'_concat.txt')
    listing.write_text(''.join("file '"+p.as_posix().replace("'", "'\\''")+f"'\nduration {length:.9f}\n" for p,length in parts),encoding='utf8')
    joined=temp/(edit['name']+'_joined.mkv')
    run(ff,['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(joined)],temp/(edit['name']+'_join.log'))
    art=artwork(plan,edit,temp);dur=edit['duration'];offset=0
    vf='[0:v]setpts=PTS-STARTPTS,fps=60[base];[base][2:v]overlay=0:0'
    for c in edit['cuts']:
        if c['replay']:
            vf+=f",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='REPLAY / {c['speed']:.2f}x':fontsize=29:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=13:x=58:y=280:enable='between(t,{offset:.6f},{offset+c['duration']-.001:.6f})'"
        offset+=c['duration']
    vf+=f",drawbox=x=60:y=1840:w=960:h=4:color=white@0.16:t=fill,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='●':fontcolor={edit['color'].replace('#','0x')}:fontsize=18:x='60+950*t/{dur}':y=1826[v]"
    # New full-range recordings must be converted, not merely tagged, to limited-range yuv420p.
    vf=vf[:-3]+',scale=in_range=auto:out_range=tv,format=yuv420p,setparams=range=limited[v]'
    a=plan['audio']
    music_eq=f'bass=g={a["music_bass_db"]}:f=100:t=q:w=0.707,' if a.get('music_bass_db') else ''
    af=f'[0:a]aresample=48000:async=1:first_pts=0,asetpts=N/SR/TB,highpass=f=75,acompressor=threshold=0.22:ratio=3:attack=3:release=90,volume={a["game_gain"]}[game];[1:a]atrim=duration={dur},asetpts=PTS-STARTPTS,aresample=48000,{music_eq}volume={a["music_gain"]},afade=t=in:d=0.008,afade=t=out:st={max(0,dur-.09)}:d=0.09[beat];[game][beat]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=0,loudnorm=I={a["target_lufs"]}:TP=-1.2:LRA=9[a]'
    run(ff,['-i',str(joined),'-ss',str(edit['music_start']),'-i',str(root/plan['music']['file']),'-loop','1','-i',str(art),'-filter_complex_threads','2','-filter_complex',vf+';'+af,'-map','[v]','-map','[a]','-t',f'{dur:.9f}',*codec(True),'-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',str(dest)],temp/(edit['name']+'_final.log'))
    print('PRONTO: '+dest.name,flush=True)
