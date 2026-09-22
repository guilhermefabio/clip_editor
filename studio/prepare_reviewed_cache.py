import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import config as C
from pipeline import features
entries=json.loads((C.ROOT/'frames/analise_20260909/inventario.json').read_text(encoding='utf8'))
for i,e in enumerate(entries):
    print(f"SOURCE {i+1}/11 {e['file']}",flush=True)
    f=features.extract(C.ROOT/e['file'],progress=lambda p,m:print(f'{p:.2f} {m}',flush=True))
    assert f['sha']==e['sha256'], 'Fonte alterada'
print('CACHE COMPLETE',flush=True)
