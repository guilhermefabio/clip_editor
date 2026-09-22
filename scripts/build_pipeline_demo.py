"""Build a minimal English GIF from real recordings, scorer output and an edit plan.

Requires private local media. Existing source videos and renders are never modified.
Example arguments are recorded privately in docs/local/demo/provenance.json.
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'harness'))
from tooling import resolve_tool

W, H, FPS = 960, 540, 10
BG, PANEL = '#0b1014', '#131b21'
WHITE, MUTED, GREEN, LINE = '#f2f5f4', '#8d9bA4', '#daff64', '#2b363e'
FONT_PATH = Path('C:/Windows/Fonts')


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_PATH / ('segoeuib.ttf' if bold else 'segoeui.ttf')), size)


def text(im, xy, value, size=18, color=WHITE, bold=False):
    ImageDraw.Draw(im).text(xy, value, font=font(size, bold), fill=color)


def frames(ff, path, start, duration, width, height):
    command = [str(ff), '-v', 'error', '-ss', str(start), '-i', str(path),
               '-t', str(duration), '-vf', f'fps={FPS},scale={width}:{height}',
               '-an', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    data = subprocess.check_output(command)
    step = width * height * 3
    return [Image.frombytes('RGB', (width, height), data[i:i+step])
            for i in range(0, len(data) - step + 1, step)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recording', type=Path, required=True)
    parser.add_argument('--scores', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--short-index', type=int, default=1)
    parser.add_argument('--output', type=Path, default=ROOT/'docs/assets/pipeline_bodycam.gif')
    args = parser.parse_args()
    ff = resolve_tool('ffmpeg')
    work = ROOT / 'docs/local/demo'
    work.mkdir(parents=True, exist_ok=True)
    plan = json.loads(args.plan.read_text(encoding='utf8'))
    edit = plan['edits'][args.short_index]
    cuts = edit['cuts'][:3]
    origins = json.loads(args.recording.with_suffix('.origens.json').read_text(encoding='utf8'))
    origin = next(s for s in origins['segments'] if s['file'] == cuts[0]['file'])
    assert all(c['file'] == origin['file'] for c in cuts)
    offset = origin['start']
    score = json.loads(args.scores.read_text(encoding='utf8'))
    assert score['file'] == args.recording.name
    timestamps = np.array(score['times']) - offset
    scores = np.array(score['smooth'])
    lower, upper = cuts[0]['start'] - 8, cuts[2]['end'] + 5
    mask = (timestamps >= lower) & (timestamps <= upper)
    tt, pp = timestamps[mask], scores[mask]
    peaks = []
    for cut in cuts:
        idx = np.flatnonzero((tt >= cut['start']) & (tt <= cut['end']))
        peaks.append(int(idx[np.argmax(pp[idx])]))
    rendered = ROOT / plan['output'] / (edit['name'] + '.mp4')
    print('Decoding real source and rendered Short...', flush=True)
    source = frames(ff, args.recording, offset + cuts[0]['start'], 2.5, 592, 250)
    previews = [frames(ff, args.recording, offset+c['start']+.6, .2, 184, 78)[0] for c in cuts]
    result = frames(ff, rendered, 0, 5.2, 180, 320)
    final_big = frames(ff, rendered, 0, 5.2, 216, 384)
    assert source and len(result) >= 50 and len(final_big) >= 50
    durations = [25, 25, 25, 30, 52]
    stages = ['Original gameplay', 'Interest curve', 'Peak selection', 'Shorts assembled', 'Final result']
    descriptions = ['Start with the full recording.', 'Score moments, frame by frame.',
                    'Find action worth keeping.', 'Bring the highlights together.', 'From raw footage to a finished Short.']
    all_frames = []

    def base(stage):
        im = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(im)
        text(im, (36, 22), 'clip_editor', 21, GREEN, True)
        text(im, (744, 28), 'BODYCAM / REAL FOOTAGE', 12, MUTED)
        text(im, (36, 61), 'From gameplay to highlights.', 30, WHITE, True)
        text(im, (38, 107), descriptions[stage], 16, MUTED)
        d.line((36, 474, 924, 474), fill=LINE)
        for i, label in enumerate(stages):
            x = 46 + i * 182
            d.ellipse((x, 496, x+7, 503), fill=GREEN if i <= stage else LINE)
            text(im, (x+15, 490), label, 13, WHITE if i == stage else MUTED, i == stage)
            if i < 4:
                d.line((x+159, 499, x+169, 499), fill=LINE, width=1)
        return im

    def portrait(im, idx, xy=(714, 139), big=False):
        # Only the demo overlay is translated; original rendered video stays intact.
        pic = (final_big if big else result)[min(idx, 45, len(result)-1)].copy()
        width, height = pic.size
        d = ImageDraw.Draw(pic)
        d.rectangle((0, 0, width, height//8), fill=BG)
        d.rectangle((0, height*7//8, width, height), fill=BG)
        f = font(9 if not big else 10, True)
        d.text((width/2, 7), 'VIEIRASPLAY', font=f, fill=GREEN, anchor='mt')
        d.text((width/2, 22), 'EVERY SECOND COUNTS', font=font(10 if not big else 11, True), fill=WHITE, anchor='mt')
        d.text((width/2, height-27), 'BODYCAM / HIGHLIGHTS', font=font(9), fill=MUTED, anchor='mt')
        im.paste(pic, xy)
        ImageDraw.Draw(im).rounded_rectangle((xy[0]-1,xy[1]-1,xy[0]+width,xy[1]+height), radius=8, outline=LINE)

    def chart(im, reveal=1., selected=0):
        d = ImageDraw.Draw(im)
        x0,y0,x1,y1 = 52, 221, 611, 400
        d.rounded_rectangle((36,155,630,447),radius=12, fill=PANEL)
        text(im,(52,171),'MODEL INTEREST SCORE',12,MUTED,True)
        text(im,(551,170),'0 â€“ 1',12,MUTED)
        for v in [0.,.5,1.]:
            y = y1-v*(y1-y0)
            d.line((x0,y,x1,y),fill=LINE)
        threshold = float(score['threshold'])
        yt = y1-threshold*(y1-y0)
        for x in range(x0,x1,10):d.line((x,yt,x+4,yt),fill='#607078')
        points=[(x0+(t-lower)/(upper-lower)*(x1-x0),y1-p*(y1-y0)) for t,p in zip(tt,pp)]
        count=max(2,int(len(points)*reveal))
        d.line(points[:count],fill=GREEN,width=3)
        for j,idx in enumerate(peaks[:selected]):
            x,y=points[idx]
            d.line((x,y+9,x,y1),fill='#788b43',width=1)
            d.ellipse((x-6,y-6,x+6,y+6),fill=GREEN)
            text(im,(x-4,y-26),str(j+1),13,WHITE,True)
        text(im,(52,417),f'{int(lower)//60:02d}:{int(lower)%60:02d}',12,MUTED)
        text(im,(476,417),'Recording time',12,MUTED)

    for stage,n in enumerate(durations):
        for k in range(n):
            im=base(stage);d=ImageDraw.Draw(im)
            progress=k/max(n-1,1)
            if stage==0:
                im.paste(source[k%len(source)],(36,166))
                d.rounded_rectangle((36,166,628,416),radius=8,outline=LINE)
                text(im,(686,192),'01 / INPUT',12,GREEN,True)
                text(im,(686,224),'Real footage.',23,WHITE,True)
                text(im,(686,258),'Real moments.',23,WHITE,True)
                text(im,(686,309),'Visual + audio signals',14,MUTED)
                text(im,(36,429),'One recording. Many possible highlights.',13,MUTED)
            elif stage in (1,2):
                selected=0 if stage==1 else min(3,1+int(progress*3))
                chart(im,min(1.,progress*1.2) if stage==1 else 1.,selected)
                if stage==1:
                    im.paste(previews[0],(712,168))
                    text(im,(686,278),'02 / ANALYZE',12,GREEN,True)
                    text(im,(686,311),'Find the signal.',22,WHITE,True)
                    text(im,(686,351),'70 features. One score.',14,MUTED)
                    text(im,(686,378),'Actual saved model output',12,MUTED)
                else:
                    for j in range(selected):
                        im.paste(previews[j],(712,158+j*93))
                        text(im,(687,184+j*93),str(j+1),14,GREEN,True)
                    text(im,(686,440),'3 selected moments',13,MUTED)
            elif stage==3:
                text(im,(36,166),'03 SELECTED CUTS',12,GREEN,True)
                for j,pic in enumerate(previews):
                    x=36+j*200
                    if progress >= j*.23:
                        im.paste(pic,(x,202))
                        text(im,(x,290),f'0{j+1}',14,MUTED)
                text(im,(36,326),'BEAT-SYNCED TIMELINE',12,MUTED,True)
                for j in range(12):
                    x=36+j*49
                    d.line((x,356,x,407),fill=LINE,width=1)
                for j in range(3):
                    if progress >= j*.23:
                        x=36+j*196
                        d.rounded_rectangle((x,365,x+186,397),radius=4,fill=GREEN)
                        text(im,(x+12,369),f'CUT 0{j+1}',12,BG,True)
                text(im,(36,426),'Keep the action. Cut the waiting.',16,WHITE)
                portrait(im,int(k/30*len(result)))
            else:
                text(im,(36,178),'05 / OUTPUT',12,GREEN,True)
                text(im,(36,220),'Ready for the',36,WHITE,True)
                text(im,(36,265),'small screen.',36,WHITE,True)
                text(im,(38,338),'Selected. Assembled. Rendered.',18,MUTED)
                text(im,(38,382),'9:16  /  FFmpeg  /  Human-reviewed workflow',13,MUTED)
                portrait(im,k,(702,78),big=True)
                d.rectangle((702,464,702+216*progress,467),fill=GREEN)
            all_frames.append(im)
        all_frames[-1].save(work/f'stage_{stage+1}.png')
    print('Encoding GIF...',flush=True)
    intermediate=work/'animation.mkv'
    proc=subprocess.Popen([str(ff),'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
                           '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','ffv1',str(intermediate)],stdin=subprocess.PIPE)
    for im in all_frames:proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait():raise RuntimeError('Intermediate encoding failed')
    candidate=work/'pipeline_bodycam.new.gif'
    subprocess.run([str(ff),'-v','error','-y','-i',str(intermediate),'-filter_complex',
                    '[0:v]split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none',
                    '-loop','0',str(candidate)],check=True)
    with Image.open(candidate) as check:
        assert check.size==(W,H) and check.n_frames>=150
        duration=sum((check.seek(i) or check.info.get('duration',0)) for i in range(check.n_frames))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    backup=work/'pipeline_bodycam.previous.gif'
    if args.output.exists() and not backup.exists():shutil.copy2(args.output,backup)
    shutil.copy2(candidate,args.output)
    provenance={'recording':str(args.recording),'score':str(args.scores),'plan':str(args.plan),
                'rendered_short':str(rendered.relative_to(ROOT)),'original_recording_offset':offset,
                'shown_cuts':cuts,'shown_peak_times':[float(tt[i]) for i in peaks],
                'duration_ms':duration,'size_bytes':args.output.stat().st_size,
                'note':'Real source frames, saved score and rendered output. English title overlays only in GIF. First three cuts illustrated; final preview holds its last readable frame for 0.6 seconds; no source video modified.'}
    (work/'provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')
    sheet=Image.new('RGB',(W*2,H*3),BG)
    for i in range(5):sheet.paste(Image.open(work/f'stage_{i+1}.png'),((i%2)*W,(i//2)*H))
    sheet.save(work/'review.png')
    print(f'Saved {args.output}: {duration/1000:.1f}s, {args.output.stat().st_size/1024/1024:.2f} MiB',flush=True)


if __name__=='__main__':main()
