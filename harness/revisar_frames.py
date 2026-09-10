"""Inventário e folhas de contato; não atribui rótulos automaticamente."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor

import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'frames' / 'analise_20260909'
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)


def inventory():
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for i, p in enumerate(sorted((ROOT / 'gravacoes').glob('*.mp4')), 1):
        data = json.loads(subprocess.check_output([
            str(ROOT / '_tools/ffprobe.exe'), '-v', 'error', '-show_streams',
            '-show_format', '-of', 'json', str(p)]))
        v = next(s for s in data['streams'] if s['codec_type'] == 'video')
        with p.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        entries.append(dict(id=i, file=p.relative_to(ROOT).as_posix(), sha256=digest,
                            width=v['width'], height=v['height'],
                            fps=v['avg_frame_rate'], frames=int(v['nb_frames']),
                            duration=float(data['format']['duration']),
                            review_status='pending'))
        print(f"Inventário {i}: {p.name}", flush=True)
    (OUT / 'inventario.json').write_text(json.dumps(entries, indent=2), encoding='utf8')
    return entries


def sheet(entry, start=0, end=None, step=3, width=480, page_size=36):
    end = min(end if end is not None else entry['duration'], entry['duration'])
    cap = cv2.VideoCapture(str(ROOT / entry['file']))
    h = round(width * entry['height'] / entry['width'])
    times = [start + j * step for j in range(math.ceil((end-start)/step))]
    folder = OUT / 'contatos'
    folder.mkdir(parents=True, exist_ok=True)
    for base in range(0, len(times), page_size):
        ts = times[base:base+page_size]
        dst = folder / f"v{entry['id']:02}_{start:g}_passo{step:g}_p{base//page_size:03}.jpg"
        if dst.exists():
            continue
        im = Image.new('RGB', (width*3, (h+26)*math.ceil(len(ts)/3)), '#151515')
        draw = ImageDraw.Draw(im)
        for j, t in enumerate(ts):
            cap.set(cv2.CAP_PROP_POS_MSEC, t*1000)
            ok, frame = cap.read()
            x, y = j%3*width, j//3*(h+26)
            if ok:
                frame = cv2.resize(frame, (width,h), interpolation=cv2.INTER_AREA)
                im.paste(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), (x,y))
            draw.text((x+4, y+h+3), f"V{entry['id']:02} {t:08.3f}s", font=FONT, fill='white')
        im.save(dst, quality=92)
        print(dst.relative_to(ROOT), flush=True)
    cap.release()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['inventory','overview','detail'])
    ap.add_argument('--video', type=int)
    ap.add_argument('--start', type=float, default=0)
    ap.add_argument('--end', type=float)
    ap.add_argument('--step', type=float, default=.25)
    args = ap.parse_args()
    if args.command == 'inventory':
        inventory()
    else:
        entries = json.loads((OUT / 'inventario.json').read_text())
        if args.command == 'overview':
            with ThreadPoolExecutor(2) as pool:
                list(pool.map(sheet, entries))
        else:
            sheet(entries[args.video-1], args.start, args.end, args.step, 800, 18)
