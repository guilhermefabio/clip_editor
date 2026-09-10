"""VieirasPlay local workflow. Run from any directory; paths are relative to BODYCAM."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse, copy, hashlib, html, json, math, re, subprocess, sys
import engine

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'harness';FF=ROOT/'_tools/ffmpeg.exe';FP=ROOT/'_tools/ffprobe.exe'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p, data):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def safe(p):
    result=(ROOT/p).resolve()
    if not result.is_relative_to(ROOT) or result==ROOT:raise ValueError(f'Caminho fora da pasta de trabalho: {p}')
    if result.relative_to(ROOT).parts[0] in ('.git','.codex','.agents','_tools'):raise ValueError('Diretório reservado')
    return result
def probe(p):
    return json.loads(subprocess.check_output([str(FP),'-v','error','-show_streams','-show_format','-of','json',str(p)]))
def history():return read(HERE/'historico.json') if (HERE/'historico.json').exists() else {'version':1,'sources':{},'batches':[]}
def inventory(sources=()):
    hist=history();groups={}
    for p in sorted(set([*ROOT.glob('clipe_*.mp4'), *ROOT.glob('clip_*.mp4'), *[safe(s) for s in sources]])):
        digest=sha(p)
        if digest in groups:groups[digest]['files'].append(p.name);continue
        meta=probe(p);v=next(s for s in meta['streams'] if s['codec_type']=='video')
        groups[digest]={'sha256':digest,'files':[p.name],'duration':float(meta['format']['duration']),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'new_content':digest not in hist['sources'],'used_intervals':len(hist['sources'].get(digest,{}).get('uses',[]))}
    report={'sources':list(groups.values())};save(HERE/'inventario.json',report)
    for g in groups.values():print(f'{"NOVO" if g["new_content"] else "CONHECIDO"}: {", ".join(g["files"])} | {g["duration"]:.1f}s | {g["used_intervals"]} trechos usados')
    return report
def init(output, destination):
    safe(output);p=safe(destination)
    if p.exists():raise ValueError(f'Plano já existe: {p}')
    defaults=read(HERE/'defaults.json');hist=history()
    numbers=[int(re.match(r'^(\d+)',e).group(1)) for b in hist['batches'] for e in b.get('shorts',[]) if re.match(r'^(\d+)',e)]
    numbers.extend(int(p.name.split('_')[0]) for folder in [*ROOT.glob('shorts_*'),*(ROOT/'cliping').glob('*')] if folder.is_dir() for p in folder.glob('*.mp4') if re.match(r'^\d+_',p.name))
    first=max(numbers,default=0)+1
    plan={'version':1,'output':output,'channel':defaults['channel'],'game':defaults['game'],'batch_size':5,'duration_range':[15,20],'music':defaults['music'],'allow_reuse':False,'edits':[]}
    for n in range(first,first+5):plan['edits'].append({'name':f'{n:02}_DEFINIR','title':'DEFINIR APÓS INSPEÇÃO','tag':'DEFINIR','color':'#DAFF64','music_start':0,'cuts':[]})
    save(p,plan);print('Plano criado: '+str(p))
def normalize(path):
    plan=copy.deepcopy(read(safe(path)));defaults=read(HERE/'defaults.json');hist=history()
    for key in ('channel','game','audio'):plan.setdefault(key,copy.deepcopy(defaults[key]))
    plan.setdefault('duration_range',[15,20]);plan.setdefault('batch_size',5)
    out=safe(plan['output'])
    if out.is_file() or out in [ROOT/'shorts_bodycam',ROOT/'shorts_bodycam_lote2',HERE]:raise ValueError('Use uma pasta nova para o lote')
    edits=plan['edits']
    if len(edits)!=plan['batch_size']:raise ValueError(f'O plano exige {plan["batch_size"]} vídeos')
    music_cache={}
    def music_info(m):
        music=safe(m['file'])
        if music not in music_cache:music_cache[music]=(probe(music),sha(music))
        musicmeta,digest=music_cache[music]
        if not any(s['codec_type']=='audio' for s in musicmeta['streams']):raise ValueError('Música sem áudio')
        if digest!=m['sha256'].lower():raise ValueError('O beat mudou. Analise a faixa e atualize hash, BPM, offset e evidência no plano.')
        bpm=float(m['bpm']);grid=float(m.get('grid_offset_seconds',0))
        if not math.isfinite(bpm) or not 30<=bpm<=300 or not math.isfinite(grid):raise ValueError('Grade musical inválida')
        if not m.get('evidence','').strip():raise ValueError('Registre a evidência da grade musical')
        return bpm,grid,float(musicmeta['format']['duration'])
    music_info(plan['music'])
    if plan.get('allow_reuse') and not plan.get('reuse_reason','').strip():raise ValueError('Reuso exige motivo explícito')
    seen=set();meta_cache={};cuts_seen=[]
    for e in edits:
        bpm,grid,duration_music=music_info(e.get('music',plan['music']))
        if not re.fullmatch(r'\d{2,}_[A-Z0-9_]+',e['name']) or e['name'] in seen:raise ValueError('Nome inválido ou repetido: '+e['name'])
        seen.add(e['name'])
        if not e.get('title') or not e.get('tag') or 'DEFINIR' in e['title']:raise ValueError('Preencha título e tema de '+e['name'])
        e.setdefault('color','#DAFF64')
        if not re.fullmatch('#[0-9a-fA-F]{6}',e['color']):raise ValueError('Cor deve ser hexadecimal')
        if not e['cuts']:raise ValueError('Selecione os cortes de '+e['name'])
        cursor=0;previous_frame=0
        for c in e['cuts']:
            p=safe(c['file'])
            if p.parent not in (ROOT,ROOT/'gravacoes') or (not p.name.startswith(('clipe_','clip_')) and c['file'] not in plan.get('sources',[])):raise ValueError('Fonte deve ser uma gameplay em gravacoes/ ou na raiz, explicitamente indicada no plano quando tiver outro nome')
            if p not in meta_cache:
                data=probe(p);v=next(s for s in data['streams'] if s['codec_type']=='video')
                if not any(s['codec_type']=='audio' for s in data['streams']):raise ValueError('Fonte sem áudio: '+p.name)
                meta_cache[p]=(float(data['format']['duration']),v['width'],v['height'],sha(p))
            available,w,h,digest=meta_cache[p];c.setdefault('speed',1);c.setdefault('center_x',.5);c.setdefault('gamma',1.08);c.setdefault('replay',False)
            numbers=[c['start'],c['beats'],c['speed'],c['center_x'],c['gamma']]
            if not all(isinstance(n,(int,float)) and math.isfinite(n) for n in numbers):raise ValueError('Valores não numéricos ou não finitos')
            if c['start']<0 or c['beats']<=0 or not .5<=c['speed']<=2 or not 0<=c['center_x']<=1 or not .5<=c['gamma']<=2:raise ValueError('Corte fora dos limites')
            if not isinstance(c['replay'],bool) or not c.get('note','').strip():raise ValueError('Registre replay booleano e motivo editorial do corte')
            cursor+=c['beats']*60/bpm;end_frame=round(cursor*60);c['frames']=end_frame-previous_frame;previous_frame=end_frame
            if c['frames']<=0:raise ValueError('Corte menor que um quadro')
            c['duration']=c['frames']/60;c['width']=w;c['height']=h;c['sha256']=digest;c['end']=c['start']+c['duration']*c['speed']
            if c['end']>available+.005:raise ValueError(f'Corte ultrapassa o fim da fonte: {p.name}')
            if not plan.get('allow_reuse'):
                for u in hist['sources'].get(digest,{}).get('uses',[]):
                    if u['batch']!=plan['output'] and min(u['end'],c['end'])-max(u['start'],c['start'])>.05:raise ValueError(f'Trecho já usado em {u["short"]}: {p.name} @ {c["start"]}')
                for other_name,other in cuts_seen:
                    if other_name!=e['name'] and digest==other['sha256'] and min(other['end'],c['end'])-max(other['start'],c['start'])>.05:raise ValueError('Mesmo confronto em dois Shorts deste lote')
            cuts_seen.append((e['name'],c))
        e['frames']=previous_frame;e['duration']=previous_frame/60
        if not plan['duration_range'][0]<=e['duration']<=plan['duration_range'][1]:raise ValueError(f'Duração fora do plano: {e["name"]} ({e["duration"]:.3f}s)')
        start=float(e['music_start'])
        if not math.isfinite(start) or start<0 or start+e['duration']>duration_music+.005:raise ValueError('Trecho de música fora do arquivo')
        phase=(start-grid)*bpm/60
        if abs(phase-round(phase))*60/bpm>1/60:raise ValueError('Entrada da música fora da grade; ajuste music_start ou grid_offset_seconds')
    return plan
def plan_digest(plan):return hashlib.sha256(json.dumps(plan,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def verify_one(plan,e):
    import cv2,numpy as np
    from PIL import Image
    out=safe(plan['output']);p=out/(e['name']+'.mp4');data=probe(p)
    v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],v['pix_fmt'])!=(1080,1920,'60/1','h264','yuv420p'):raise ValueError('Formato de vídeo incorreto')
    if int(v['nb_frames'])!=e['frames'] or abs(float(data['format']['duration'])-e['duration'])>.045:raise ValueError('Frames ou duração incorretos')
    if a['codec_name']!='aac' or int(a['sample_rate'])!=48000 or a['channels']!=2:raise ValueError('Formato de áudio incorreto')
    decoded=subprocess.run([str(FF),'-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True)
    if decoded.returncode or decoded.stderr:raise ValueError(decoded.stderr)
    raw=subprocess.check_output([str(FF),'-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-']);peak=float(np.max(np.abs(np.frombuffer(raw,np.float32))))
    if not 0<peak<1:raise ValueError('Áudio silencioso ou com clipping')
    levels=subprocess.run([str(FF),'-hide_banner','-i',str(p),'-vn','-af','loudnorm=I=-14:TP=-1:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    levels=json.JSONDecoder().raw_decode(levels[levels.rfind('{'):])[0];lufs=float(levels['input_i']);tp=float(levels['input_tp'])
    if not plan['audio']['min_lufs']<=lufs<=plan['audio']['max_lufs'] or tp>plan['audio']['max_true_peak_db']:raise ValueError(f'Mixagem fora do alvo: {lufs} LUFS, {tp} dBTP')
    folder=out/'projeto/analise';folder.mkdir(parents=True,exist_ok=True);cap=cv2.VideoCapture(str(p));sheet=Image.new('RGB',(1620,480))
    for i,fraction in enumerate([.03,.19,.37,.56,.84,.985]):
        cap.set(cv2.CAP_PROP_POS_MSEC,e['duration']*fraction*1000);ok,frame=cap.read()
        if not ok:raise ValueError('Falha ao extrair quadro')
        im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));sheet.paste(im.resize((270,480)),(270*i,0))
        if i==0:im.resize((540,960)).save(out/(e['name']+'.jpg'),quality=90)
    cap.release();sheet.save(folder/(e['name']+'_revisao.jpg'),quality=90)
    return {'file':p.name,'sha256':sha(p),'duration':float(data['format']['duration']),'frames':int(v['nb_frames']),'loudness_LUFS':lufs,'true_peak_dBTP':tp,'decode':'OK'}
def verify(plan):
    out=safe(plan['output'])
    with ThreadPoolExecutor(2) as pool:results=list(pool.map(lambda e:verify_one(plan,e),plan['edits']))
    report={'status':'passed','plan_sha256':plan_digest(plan),'videos':results};save(out/'projeto/verificacao.json',report)
    cards=[]
    for e in plan['edits']:
        n=e['name'];cards.append(f'<article><video controls playsinline preload="none" poster="{n}.jpg" src="{n}.mp4"></video><div><h2>{html.escape(e["title"])}</h2><p>{html.escape(e["tag"])} · {e["duration"]:.1f} s</p><a download href="{n}.mp4">Baixar MP4 ↓</a></div></article>')
    page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>VieirasPlay — Shorts</title><style>*{box-sizing:border-box}body{margin:0;padding:40px 24px;background:#101114;color:#f6f7f3;font:16px system-ui,sans-serif}header,main{max-width:1440px;margin:auto}header{margin-bottom:30px}h1{color:#daff64}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}article{background:#1b1d23;border:1px solid #30323a;border-radius:14px;overflow:hidden}video{width:100%;aspect-ratio:9/16;display:block;background:black}article div{padding:18px}h2{font-size:16px}p{color:#b5b6c0}a{color:#daff64;text-decoration:none}</style><header><h1>VieirasPlay / Shorts</h1><p>1080 × 1920 · 60 fps · Phonk + gameplay</p></header><main>'''+''.join(cards)+'''</main><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()})))</script></html>'''
    (out/'ASSISTIR.html').write_text(page,encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
    return report
def record(plan):
    out=safe(plan['output']);report=read(out/'projeto/verificacao.json');review=out/'projeto/revisao_editorial.md'
    if report['status']!='passed' or report['plan_sha256']!=plan_digest(plan):raise ValueError('Validação técnica ausente ou desatualizada')
    if not review.exists() or len(review.read_text(encoding='utf8').strip())<30:raise ValueError('O agente deve registrar sua revisão editorial e visual antes de arquivar o lote')
    for v in report['videos']:
        if sha(out/v['file'])!=v['sha256']:raise ValueError('MP4 mudou após a verificação')
    hist=history()
    for src in hist['sources'].values():src['uses']=[u for u in src['uses'] if u['batch']!=plan['output']]
    for e in plan['edits']:
        for c in e['cuts']:
            src=hist['sources'].setdefault(c['sha256'],{'files':[],'uses':[]})
            if c['file'] not in src['files']:src['files'].append(c['file'])
            src['uses'].append({'batch':plan['output'],'short':e['name'],'start':c['start'],'end':c['end'],'replay':c['replay']})
    hist['batches']=[b for b in hist['batches'] if b['output']!=plan['output']]
    hist['batches'].append({'output':plan['output'],'shorts':[e['name'] for e in plan['edits']]});save(HERE/'historico.json',hist)
    save(out/'projeto/registro.json',{'plan_sha256':plan_digest(plan),'status':'recorded'});print('Lote registrado no histórico.')
def clean(plan):
    out=safe(plan['output']);registration=read(out/'projeto/registro.json')
    if registration['plan_sha256']!=plan_digest(plan):raise ValueError('Lote não registrado com este plano')
    # Recheck verified final files immediately before deleting expendable intermediates.
    report=read(out/'projeto/verificacao.json')
    for v in report['videos']:
        if sha(out/v['file'])!=v['sha256']:raise ValueError('Final ausente ou alterado')
    temp=(out/'projeto/render').resolve();removed=0
    if not temp.is_relative_to(out.resolve()):raise ValueError('Diretório temporário inválido')
    for p in temp.glob('*.mkv'):
        if p.is_symlink() or p.resolve().parent!=temp:raise ValueError('Arquivo temporário fora do lote')
        removed+=p.stat().st_size;p.unlink()
    print(f'Intermediários liberados: {removed/1e6:.1f} MB')
def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='command',required=True)
    inv=commands.add_parser('inventory');inv.add_argument('--source',action='append',default=[]);i=commands.add_parser('init');i.add_argument('--output',required=True);i.add_argument('--plan',required=True)
    for name in ('check','render','verify','record','clean'):
        sub=commands.add_parser(name);sub.add_argument('plan')
        if name=='render':sub.add_argument('--encoder',choices=['h264_nvenc','libx264'],default='h264_nvenc')
    args=parser.parse_args()
    if args.command=='inventory':inventory(args.source);return
    if args.command=='init':init(args.output,args.plan);return
    plan=normalize(args.plan);out=safe(plan['output'])
    if args.command=='check':
        print('Plano válido: '+', '.join(f'{e["name"]} ({e["duration"]:.3f}s)' for e in plan['edits']));return
    if args.command=='render':
        if any((out/(e['name']+'.mp4')).exists() for e in plan['edits']):raise ValueError('Já existe MP4 de destino; use outra pasta para uma revisão')
        save(out/'projeto/edicao.json',plan)
        for e in plan['edits']:engine.render(ROOT,plan,e,args.encoder)
    elif args.command=='verify':verify(plan)
    elif args.command=='record':record(plan)
    elif args.command=='clean':clean(plan)
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,FileNotFoundError,RuntimeError,subprocess.CalledProcessError) as exc:
        print('ERRO: '+str(exc),file=sys.stderr);sys.exit(1)
