"""Amostragem rastreável e exportação de rótulos anotados por revisão visual.

Não usa scores, áudio ou cortes de Shorts para criar rótulos.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
import argparse
import csv
import hashlib
import json
import math
import shutil

import av
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'frames/analise_20260909'
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 17)


def read(p):
    return json.loads(Path(p).read_text(encoding='utf8'))


def save(p, d):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf8')


def sample(entry):
    vid = entry['id']
    folder = OUT / 'amostras' / f'v{vid:02}'
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / 'concluido.json').exists():
        return
    rows, pts_rows = [], []
    target = 0
    with av.open(str(ROOT / entry['file'])) as cont:
        st = cont.streams.video[0]
        st.thread_type = 'AUTO'
        for n, frame in enumerate(cont.decode(st)):
            t = float(frame.pts * frame.time_base)
            pts_rows.append([n, frame.pts, t])
            if t + 1e-8 < target / 3:
                continue
            dst = folder / f'v{vid:02}_f{n:07}.jpg'
            frame.reformat(width=1280, height=540, format='rgb24').to_image().save(dst, quality=94, subsampling=0)
            rows.append(dict(sample=len(rows), source_frame=n, pts=frame.pts,
                             time_base=str(frame.time_base), time=t,
                             file=dst.relative_to(ROOT).as_posix()))
            target = math.floor(t * 3 + 1e-7) + 1
    save(folder / 'index.json', rows)
    save(folder / 'pts.json', pts_rows)
    save(folder / 'concluido.json', dict(decoded=len(pts_rows), samples=len(rows),
                                       expected=entry['frames'], sha256=entry['sha256']))
    sheets(vid)
    print(f'V{vid:02}: {len(pts_rows)} decodificados; {len(rows)} amostras', flush=True)


def sheets(vid, rows=None, name='geral', width=480, columns=4, per=48):
    folder = OUT / 'amostras' / f'v{vid:02}'
    rows = rows if rows is not None else read(folder / 'index.json')
    dest = OUT / 'revisao'
    dest.mkdir(parents=True, exist_ok=True)
    h = round(width * 1080 / 2560)
    for base in range(0, len(rows), per):
        dst = dest / f'v{vid:02}_{name}_p{base//per:03}.jpg'
        if dst.exists():
            continue
        group = rows[base:base+per]
        im = Image.new('RGB', (width*columns, (h+26)*math.ceil(len(group)/columns)), '#171717')
        draw = ImageDraw.Draw(im)
        for j, row in enumerate(group):
            x, y = j%columns*width, j//columns*(h+26)
            with Image.open(ROOT / row['file']) as src:
                im.paste(src.resize((width,h), Image.Resampling.LANCZOS), (x,y))
            draw.text((x+3,y+h+3), f"V{vid:02} S{row['sample']:04} {row['time']:08.3f}s", fill='white', font=FONT)
        im.save(dst, quality=93)


def detail(entry, start, end):
    vid = entry['id']
    general = OUT / 'amostras' / f'v{vid:02}'
    mapping = {r[1]:r[0] for r in read(general/'pts.json')}
    name = f'd{start:g}_{end:g}'
    folder = OUT / 'detalhes' / f'v{vid:02}_{name}'
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    target = start
    with av.open(str(ROOT / entry['file'])) as cont:
        st = cont.streams.video[0]
        cont.seek(max(0,int(start / st.time_base)), stream=st, backward=True)
        for frame in cont.decode(st):
            t = float(frame.pts * frame.time_base)
            if t + 1e-8 < target:
                continue
            if t >= end:
                break
            n = mapping[frame.pts]
            dst = folder / f'v{vid:02}_f{n:07}.jpg'
            frame.reformat(width=1280, height=540, format='rgb24').to_image().save(dst, quality=95, subsampling=0)
            rows.append(dict(sample=len(rows), source_frame=n, pts=frame.pts,
                             time_base=str(frame.time_base), time=t,
                             file=dst.relative_to(ROOT).as_posix()))
            target = start + (math.floor((t-start)*10+1e-7)+1)/10
    save(folder/'index.json',rows)
    sheets(vid, rows, name, width=640, columns=3, per=18)
    print(f'V{vid:02} detalhe {start}-{end}: {len(rows)} frames a 10 fps',flush=True)


def export(plan):
    entries = {e['id']:e for e in read(OUT/'inventario.json')}
    result, skipped = [], []
    seen = set()
    for review in plan['videos']:
        vid = review['id']
        entry = entries[vid]
        rows = read(OUT/'amostras'/f'v{vid:02}'/'index.json')
        complete_pages = set(review['reviewed_pages'])
        for row in rows:
            why = next((e['reason'] for e in review['exclude'] if e['start'] <= row['time'] < e['end']), None)
            if row['sample']//48 not in complete_pages:
                why = 'pagina_ainda_nao_revisada'
            if why:
                skipped.append(dict(video=vid,**row,reason=why))
                continue
            result.append(dict(video=vid,**row,label='nada',event='',evidence=review['negative_evidence']))
        for event in review['events']:
            detail_rows = read(OUT/'detalhes'/f"v{vid:02}_d{event['start']:g}_{event['end']:g}"/'index.json')
            for sample_id in event['keep_samples']:
                row = detail_rows[sample_id]
                if not any(e['start'] <= row['time'] < e['end'] for e in review['exclude']):
                    raise ValueError('Evento deve ser excluído da amostragem negativa')
                result.append(dict(video=vid,**row,label='kill',event=event['id'],evidence=event['evidence']))
    digest_seen = {}
    final = []
    for row in result:
        entry = entries[row['video']]
        key = (entry['sha256'],row['source_frame'])
        if key in seen:
            raise ValueError(f'Frame duplicado entre rótulos: {key}')
        seen.add(key)
        src = ROOT / row['file']
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if digest in digest_seen:
            if digest_seen[digest] != row['label']:
                raise ValueError('Conteúdo idêntico com rótulos conflitantes')
            skipped.append(dict(**row,reason='jpeg_duplicado_exato'))
            continue
        digest_seen[digest] = row['label']
        dst = ROOT / 'frames' / row['label'] / f"gt_{entry['sha256'][:12]}_f{row['source_frame']:07}.jpg"
        if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Destino existente diferente: {dst}')
        if not dst.exists():
            shutil.copy2(src,dst)
        final.append(dict(file=dst.relative_to(ROOT).as_posix(),label=row['label'],video=row['video'],
                          source=entry['file'],source_sha256=entry['sha256'],
                          source_frame=row['source_frame'],pts=row['pts'],time_base=row['time_base'],
                          time=row['time'],event=row['event'],evidence=row['evidence'],image_sha256=digest))
    with (OUT/'manifesto.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f,fieldnames=list(final[0]) if final else ['file','label'])
        writer.writeheader();writer.writerows(final)
    save(OUT/'excluidos.json',skipped)
    save(OUT/'exportacao.json',dict(total=len(final),kill=sum(r['label']=='kill' for r in final),
                                   nada=sum(r['label']=='nada' for r in final),skipped=len(skipped)))
    print(read(OUT/'exportacao.json'))


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('command',choices=['sample','detail','export'])
    ap.add_argument('--video',type=int)
    ap.add_argument('--start',type=float)
    ap.add_argument('--end',type=float)
    a=ap.parse_args()
    entries=read(OUT/'inventario.json')
    if a.command=='sample':
        chosen=[e for e in entries if not a.video or e['id']==a.video]
        with ThreadPoolExecutor(2) as pool:
            list(pool.map(sample,chosen))
    elif a.command=='detail':
        detail(entries[a.video-1],a.start,a.end)
    else:
        export(read(OUT/'rotulos.json'))
