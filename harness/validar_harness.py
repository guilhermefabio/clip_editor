"""Focused regression checks plus one short real encode across both source geometries."""
import copy,json
from shorts import ROOT,HERE,read,save,normalize,verify,engine,safe

def main():
    folder=HERE/'validation';folder.mkdir(exist_ok=True)
    example=read(HERE/'examples/lote2_aprovado.json');results=[]
    valid=normalize('harness/examples/lote2_aprovado.json')
    assert [e['frames'] for e in valid['edits']]==[1200,1200,1300,1200,1200]
    assert {c['width'] for e in valid['edits'] for c in e['cuts']}=={1708,2560}
    results.append('Referência aprovada: frames e resoluções preservados')
    def reject(label,change):
        p=copy.deepcopy(example);change(p);path=folder/'invalid_plan.json';save(path,p)
        try:normalize(str(path))
        except ValueError:results.append(label);return
        raise AssertionError('Plano inválido foi aceito: '+label)
    reject('Hash de música alterado rejeitado',lambda p:p['music'].update(sha256='0'*64))
    reject('Reuso acidental de trecho anterior rejeitado',lambda p:p.update(allow_reuse=False))
    reject('Corte fora da fonte rejeitado',lambda p:p['edits'][0]['cuts'][0].update(start=99999))
    reject('Destino fora do workspace rejeitado',lambda p:p.update(output='../escape'))
    reject('Export não aceito como gameplay',lambda p:p['edits'][0]['cuts'][0].update(file='SHORT_1.mp4'))
    # Non-integer frames per beat must use cumulative rounding, not a fixed 25 frames.
    fractional=copy.deepcopy(example);fractional['music']['bpm']=143;fractional['music']['evidence']='Grade artificial somente para teste de quantização.'
    for e in fractional['edits']:e['music_start']=0
    save(folder/'fractional_plan.json',fractional);fp=normalize(str(folder/'fractional_plan.json'))
    for e in fp['edits']:assert sum(c['frames'] for c in e['cuts'])==round(sum(c['beats'] for c in e['cuts'])*60/143*60)
    results.append('BPM com frações de quadro: duração cumulativa sem deriva')
    smoke=copy.deepcopy(example);smoke.update(output='harness/validation/render',batch_size=1,duration_range=[1,3],reuse_reason='Validação técnica do harness; não é novo Short para publicação.')
    a=copy.deepcopy(example['edits'][1]['cuts'][0]);a.update(beats=2)
    b=copy.deepcopy(example['edits'][0]['cuts'][3]);b.update(beats=2,speed=.75,replay=True)
    smoke['edits']=[{'name':'00_VALIDACAO','title':'VALIDAÇÃO DO HARNESS','tag':'TESTE DE ENQUADRAMENTO','color':'#DAFF64','music_start':0,'cuts':[a,b]}]
    save(folder/'smoke_plan.json',smoke);sp=normalize(str(folder/'smoke_plan.json'));dest=safe(sp['output'])
    save(dest/'projeto/edicao.json',sp)
    if not (dest/'00_VALIDACAO.mp4').exists():engine.render(ROOT,sp,sp['edits'][0])
    report=verify(sp);assert report['videos'][0]['frames']==100
    results.append('Encode real 1080x1920/60 fps com duas resoluções, replay, áudio e revisão técnica')
    try:engine.render(ROOT,sp,sp['edits'][0])
    except ValueError:results.append('Sobrescrita de arquivo final recusada')
    else:raise AssertionError('Sobrescrita indevidamente aceita')
    save(folder/'resultado.json',{'status':'passed','checks':results})
    print(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
