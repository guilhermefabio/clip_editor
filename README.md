# VieirasPlay — BODYCAM Studio

Editor local de gameplay para montar Shorts com a identidade VieirasPlay.
O Studio analisa gravações, sugere momentos, permite ajustar os cortes e usa
o harness para renderizar e validar os vídeos.

## Executar

```powershell
python -m pip install -r studio/requirements.txt
python studio/app.py
```

Abra http://127.0.0.1:8765. Após atualizar o código, pare o servidor com
`Ctrl+C`, execute novamente e atualize a página com `Ctrl+F5`.

O ambiente de referência usa Python 3.13. Instale FFmpeg e FFprobe em
`_tools/` seguindo [as instruções locais](_tools/LEIA.txt). Gravações, músicas,
pesos YOLO e modelos treinados são arquivos locais, não incluídos no Git.
Veja [configuração, dependências e treinamento](studio/README.md) antes da
primeira análise em uma máquina nova.

## Unir vídeos antes da edição

Em **Fonte → Unir vídeos antes da edição**, adicione as gravações, ajuste a
ordem e clique em **Unir vídeos**. O resultado fica selecionado para análise.
Os originais e o áudio são preservados. A preparação atual recodifica os
vídeos e pode demorar; ainda não há um modo de união rápida sem recodificação.
O plano de edição referencia os arquivos originais para manter o histórico.

## Testes

```powershell
python -m pytest -c studio/pytest.ini studio/tests
```

Os testes de união usam FFmpeg e FFprobe para gerar vídeos pequenos e
verificar a ordem, o áudio, o tratamento de falhas e o mapeamento das origens.

## Documentação

- [Studio: operação e modelo de interesse](studio/README.md)
- [Harness: padrão editorial e renderização](harness/README.md)
- [Integração opcional com YouTube](studio/youtube/README.md)

O Git guarda código, documentação e planos. Vídeos, caches, logs, pesos de
modelos e credenciais permanecem locais. Criar os vídeos não os publica no
YouTube.
