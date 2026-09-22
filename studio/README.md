# BODYCAM Studio

Ambiente web **local** que analisa uma gravação de gameplay, marca os momentos
de interesse com um modelo treinado nos lotes já aprovados, monta os Shorts no
padrão VieirasPlay e renderiza pelo harness existente.

**Nada aqui usa LLM.** O texto (título), o tema e o nome de cada Short são
digitados por você. O modelo só aponta *onde* estão os bons momentos.

> Coleta de métricas do YouTube (feedback real dos Shorts para modelos de
> ranking): **[studio/youtube/README.md](youtube/README.md)**. Subsistema
> desacoplado — OAuth 2.0, Data API v3 + Analytics API, snapshots históricos em
> SQLite, CLI `python studio/youtube/collector.py`.

---

## 1. Como rodar

```powershell
# a partir da pasta BODYCAM, uma vez:
pip install -r studio/requirements.txt

# sempre que quiser usar:
python studio/app.py
```

Abre em **http://127.0.0.1:8765**. É um servidor só de `localhost`, sem login,
sem nada saindo da máquina. Para parar: `Ctrl+C` na janela.

### Pastas (BODYCAM/)

| pasta | o que guarda |
|---|---|
| `gravacoes/` | gravações brutas de gameplay (`.mkv`/`.mp4`). Fonte de análise e de negativos de treino. O studio também aceita arquivo solto na raiz. |
| `clipes_kill/` | clipes crus de 10–15 s do momento do abate — positivos de treino. |
| `frames/kill/` · `frames/nada/` | **prints** rotulados (imagem parada). Uma foto = uma linha de features → `studio/pipeline/imgset.py`. |
| `cliping/lote<n>/` | saída dos lotes: Shorts finais + `projeto/edicao.json`. Lotes antigos seguem em `shorts_bodycam*/`. |
| `studio/model/kill_refs/` | prints de kill para calibrar as ROIs / o verde de aliado. |

Pré-requisitos que já estão na máquina: Python 3.13, `_tools/ffmpeg.exe` /
`ffprobe.exe`, `torch` (CPU), `opencv`, `scipy`, `pillow`. O `pip install` acima
acrescenta `fastapi`, `uvicorn`, `scikit-learn`, `joblib` e `ultralytics` (YOLO).
Os pesos `studio/model/yolov8n.pt` já estão baixados.

---

## 2. Fluxo na página

Em **Fonte → Unir vídeos antes da edição**, adicione duas ou mais gravações,
ordene com ↑/↓ e clique em **Unir vídeos**. Ao terminar, o arquivo unido fica
selecionado: clique em **Analisar** e siga o fluxo normal. Vídeos curtos também
aparecem na seleção.

A união cria `gravacoes/unidos_<id>.mp4` e um mapa `.origens.json`, preservando
os arquivos originais. Mantém o áudio da gameplay; trechos sem áudio recebem
silêncio. Normaliza resolução e FPS pela primeira gravação (até 60 fps), com
barras quando necessário, sem esticar a imagem. A preparação recodifica em
H.264 e pode demorar em gravações longas. Cópias idênticas são recusadas pelo
SHA-256. Para renderizar e registrar o histórico, o plano volta aos arquivos e
tempos originais. Um corte que atravesse a junção exige ajuste na timeline.

| # | Seção | O que fazer |
|---|---|---|
| 1 | **Fonte** | Escolher a gravação (`.mkv`/`.mp4` em `gravacoes/` ou na raiz) e clicar **Analisar**. Roda uma vez por arquivo; o resultado fica em `studio/cache/<sha>/`. Um vídeo de 40 min leva ~6–8 min (YOLO em CPU); um clipe de 1–2 min, segundos. |
| 2 | **Curva de interesse** | O gráfico mostra o score por segundo (verde), a linha de corte (vermelho tracejado) e os candidatos (azul). Clique na curva para espiar um frame. Ajuste **Shorts no lote**, **Cortes por short**, **Espalhamento** (quanto vasculhar em volta de cada região quente para pôr cada corte num pico próprio — maior = mais tempo morto descartado), a **Faixa de áudio** e a **Entrada (beats)** e clique **Agrupar automaticamente**. |
| 3 | **Shorts** | Cada card traz a miniatura do pico e os campos **Nome**, **Título**, **Tema/tag**, **Cor**, **Beats/corte**, **Faixa** (override) e **Entrada** (override). A lista de cortes tem nudge de ±0,5 s, replay, "ver" (atualiza a miniatura) e remover. A duração fica **verde** entre 20 e 22 s, **vermelha** fora. **＋ corte** adiciona um corte no fim. |
| 4 | **Gerar plano** | Grava `harness/plano_<lote>.json` e roda o `check` do harness. Mostra "✓ plano válido" ou o erro exato. Só com o plano válido o botão **Renderizar** libera. |
| 5 | **Renderização** | Chama `shorts.py render` e depois `verify` (barra + log ao vivo). |
| 6 | **Revisão** | Grade com os MP4 prontos, miniatura (`<nome>.jpg`), LUFS medido e link para o `ASSISTIR.html` do lote. |

---

## 3. A faixa de áudio

O seletor lista todo `.wav`/`.mp3` de `audio/` (e da raiz, por compatibilidade).

- **Faixas com grade conhecida** (BPM + offset já confirmados em `defaults.json`
  ou num plano aprovado) entram prontas. Hoje:

  | arquivo | BPM | offset da grade |
  |---|---|---|
  | `beat_phonk.wav` | 144 | 0 |
  | `bodycam_hook_dark_phonk.wav` | 140 | 0,045 s |
  | `slow_dark_russian_phonk.mp3` | 130 | 0,917 s |
  | `slow_dark_russian_phonk1.mp3` | 148 | 1,217 s |

- **Faixa sem grade conhecida** (hoje: `phonk_fps.wav`): aparece o botão
  **Analisar batida**. Ele estima o BPM/fase pelo envelope de percussão
  (>1800 Hz) e mostra os melhores candidatos. Você escolhe um; a evidência da
  medição vai junto no plano — o harness recusa faixa sem evidência.

- **Entrada (beats)**: onde a música começa dentro do Short. É sempre
  `offset_da_grade + n · 60/BPM`, então cai na batida. Se `n` grande fizer a
  música passar do fim do arquivo, recua sozinho de 4 em 4 beats.

- **Comprimento do corte segue o BPM da faixa.** Como `duração = beats · 60/BPM`,
  6 cortes de 8 beats só dão 20 s a 144 BPM. Para outra faixa o `fit_grid`
  escolhe nº de cortes × beats para o Short cair em 20–22 s na grade dela:

  | BPM | escolha | total |
  |---|---|---|
  | 144 | 6 × 8 beats | 20,00 s |
  | 140 | 6 × 8 beats | 20,57 s |
  | 130 | 5 × 9 beats | 20,77 s |
  | 148 | 6 × 9 beats | 21,89 s |

- Cada Short pode ter **faixa e entrada próprias** no card (útil para variar,
  como o lote 15 fez com dois beats diferentes).

---

## 4. O modelo de interesse

- **YOLO pré-treinado (COCO, `yolov8n`)** roda como está e dá, por frame:
  `person_count/conf/area/center/area_sum`. Antes de contar, cada caixa passa
  por um filtro de plausibilidade (`PERSON_MIN_CONF`, `PERSON_MAX_AREA` em
  `config.py`) — sem isso, telas sem gameplay (o tablet de loadout aberto,
  matchmaking) viram uma "pessoa" gigante e de baixa confiança cobrindo quase
  a tela toda. Cada caixa que sobra é classificada **aliado × inimigo** pelo
  contorno verde do HUD (aliado tem, inimigo não) — daí `enemy_count/area/center`,
  que é o que interessa numa cena de kill.
- Mais features baratas a **3 fps**: movimento global e central, brilho,
  contraste, saturação, fração de vermelho, de flash, de escuro, densidade de
  borda, `friendly_green` (quanto do verde de aliado aparece na tela); 3 bandas
  de áudio (RMS, agudos, graves); e o **sinal de kill** `hit_center` (excesso
  de bordas no centrinho — ticks do hitmarker). Bodycam não tem killfeed na
  tela, então não existe ROI pra isso.
- `derive.py` acrescenta **máx e média em janela de ±1,5 s** de cada sinal e o
  **pico acima da linha de base local** (~±4 s) de flash, vermelho, agudos,
  graves, área de inimigo e `hit_center` — o que sobe num kill e **não** sobe
  na caminhada; mais `idle_flag` e `walk_flag`. Total: **70 features**.
- **Scorer** = `HistGradientBoostingClassifier` (scikit-learn). Treina em
  **gameplay cru** (sem Shorts renderizados, sem música, áudio dentro):
  - **positivos** = frames dos **clipes de kill** (`clipes_kill/*.mp4`, 10–15 s
    cortados crus da gravação em volta do abate) + frames dentro dos cortes
    aprovados dos `*/projeto/edicao.json`;
  - **negativos** = frames bem fora dos cortes, na mesma gravação (do arquivo
    **ou do cache** `cache/<sha>/`) — caminhada, menu, loot, tempo morto;
  - `HistGradientBoosting` lida com `NaN`, então um cache antigo sem as colunas
    novas ainda entra (as colunas faltantes viram `NaN`).
- Checkbox **"ignorar clipes de kill"** (`--raw-only`): treina só nas gravações
  com cortes aprovados.
- **ROIs / verde de aliado são provisórios** — `KILL_ROI_*` e
  `FRIENDLY_GREEN_*` em `config.py`, calibrar com um print real em
  `studio/model/kill_refs/`.
- `group.py` acha os **picos** da curva suavizada, agrupa candidatos próximos
  (janela de 12 s) e escolhe as regiões mais quentes. Dentro de cada região
  (largura = **Espalhamento** × o tamanho do Short, padrão 2,2×) ele põe cada
  corte num **sub-pico próprio** e os ordena no tempo — a caminhada/recarga
  entre eles fica de fora, como nos lotes montados à mão. Só cai em bloco
  contíguo quando a região não tem sub-picos distintos suficientes.
  **Espalhamento 1×** volta ao comportamento antigo (bloco de ~20 s corridos).
  Cortes de Shorts diferentes nunca se sobrepõem.

### Painel "0 · Modelo de interesse" (na página)

Mostra os indicadores lidos de `studio/model/scorer_meta.json`:

- **ROC-AUC / average precision** na validação — `GroupKFold` por fonte quando há
  ≥2 gravações, senão hold-out temporal (últimos 25 % de uma fonte só);
- **precisão / recall / F1** no threshold sugerido;
- positivos / negativos, nº de features, nº de fontes, fps de análise;
- tabela das **fontes de treino** (cortes, duração, se veio só do cache);
- **peso das features** (permutation importance) em barras.

**Retreinar**: botão **Treinar / retreinar** no painel, ou
`python studio/pipeline/train.py`. Junta as **gravações brutas** (cortes
aprovados = positivo, resto = negativo) com os **clipes de kill** de
`clipes_kill/` (10–15 s crus, todo frame positivo). Áudio dentro. Usa o **cache
de features** (`studio/cache/<sha>/`) quando a gravação sumiu do disco.
`scorer_meta.json` grava `raw_only`, `source`, `n_kill_clips` e `audio_used`.

**Ignorar clipes de kill** (checkbox, ou `python studio/pipeline/train.py
--raw-only`): treina só nas gravações com cortes aprovados.

> Por que mudou de novo (2026-09-09): treinar só nos Shorts renderizados de
> `melhores_shorts/` deu 262 linhas, sem negativo real de gameplay e com o áudio
> descartado — o modelo virou "tem borrão de pessoa = interessante" e não pegava
> kill. Agora o positivo é gameplay **cru** do abate (mesmo domínio que o modelo
> pontua) e o negativo é caminhada/menu/loot real. As features `enemy_*` e
> `hit_center` miram o kill em si — mas dependem de calibrar a ROI e o verde de
> aliado com um print (`studio/model/kill_refs/`).

---

## 5. Estado de hoje (2026-09-07) — leia isto

- **A gravação de 40 min foi removida do disco** durante a sessão; no lugar
  entrou `clipe_1.788.818.119.254.mp4` (91 s). Mas o **cache de features dela
  sobreviveu** (`studio/cache/450d43fb…/`), então `train.py` ainda a usa — hoje
  o treino roda com 2 fontes (mkv via cache + clipe).
  - As gravações antigas (`clipe_*` / `clip_*` dos lotes 1–8) **não estão no
    disco nem no `shorts_bodycam.zip`** (o zip só tem os Shorts renderizados) e
    também não têm cache — essas não dá para recuperar para treino.
  - A transferência entre fontes ainda é ruim (AUC ≈ 0,48). Traga mais gravações
    variadas com cortes aprovados para a raiz e retreine.
- **`shorts_bodycam_lote16/`** apareceu parcial (só `projeto/`, sem MP4), com
  edits `71_AUTO`, `72_AUTO`… — nomes que o próprio studio gera. Ou seja, o
  studio já foi usado da outra máquina. Esse lote **não foi mexido** por aqui.
- O servidor `:8765` está no ar com o código atual (com a faixa de áudio).

### O que funciona ponta a ponta (testado)

analisar → curva → agrupar → escolher faixa (inclusive não-144 BPM) →
gerar plano → `check` do harness aprova → `render` + `verify` → grade de revisão
com MP4 a −14 LUFS.

### O que ainda é bruto

- Modelo de fonte única (ver acima).
- YOLO é detector pré-treinado usado como *feature*, não treinado com caixas
  suas.
- `find_peaks` acha regiões quentes e o **Espalhamento** já põe cada corte no
  seu sub-pico (descartando o tempo morto entre eles); o recorte fino de ±0,5 s
  ainda é seu, na timeline. Com o scorer atual fraco (AUC ≈ 0,54) os sub-picos
  são pista fraca — o ganho grande vem de retreinar com **gravações brutas** e
  as features de pico de combate.
- Sem desfazer/refazer na página; recarregar zera o estado (o cache em disco
  fica).

---

## 6. Arquivos

| caminho | papel |
|---|---|
| `config.py` | caminhos e constantes (fps, `KILL_ROI_HITMARKER`, `FRIENDLY_GREEN_*`, `KILL_CLIPS_DIR`…) |
| `pipeline/features.py` | decodifica a fonte 1× via ffmpeg → 22 features base (inclui `enemy_*`, `hit_center`, `friendly_green`) → `cache/<sha>/features.npz` |
| `pipeline/derive.py` | features temporais: janela ±1,5 s, picos locais de kill, `idle_flag`, `walk_flag` → 70 |
| `pipeline/dataset.py` | colhe as linhas: `clipes_kill/*.mp4` + `*/projeto/edicao.json` (positivo) e o fora-dos-cortes (negativo) |
| `pipeline/imgset.py` | prints de `frames/kill` `frames/nada` → `model/frames_dataset.csv` + `.npz`; `--train` treina `scorer_frames.joblib` |
| `pipeline/train.py` | treina e calibra o scorer → `model/scorer.joblib` + `scorer_meta.json` |
| `pipeline/score.py` | aplica o modelo → `cache/<sha>/score.json` |
| `pipeline/group.py` | picos → candidatos → Shorts rascunho; `fit_grid`, `music_start_for` |
| `pipeline/beatgrid.py` | registro de faixas + estimativa de BPM/fase |
| `pipeline/planbuild.py` | escreve `harness/plano_<lote>.json` e roda o `check` |
| `pipeline/media.py` | extrai frames avulsos para a UI |
| `app.py` | servidor FastAPI + API |
| `web/index.html`, `web/app.js` | a página (uma só) |
| `model/` | `yolov8n.pt`, `scorer.joblib`, `scorer_meta.json` |
| `cache/<sha>/` | features, score e frames por gravação; `sources.json` é o índice |
| `model/kill_refs/` | prints de kill para calibrar `KILL_ROI_*` / `FRIENDLY_GREEN_*` |
| `tests/pipeline/` | testes do dataset (clipes de kill + gravações) e do `derive.augment` |
| `notebooks/modelo_elementos.ipynb` | mostra, com dados reais, os elementos que o scorer lê por frame + roda os testes |

### Comandos equivalentes (sem a página)

```powershell
python studio/pipeline/features.py "<video>"        # só extrai features
python studio/pipeline/train.py                     # treina o scorer
python studio/pipeline/score.py "<video>"           # gera a curva de interesse
python studio/pipeline/group.py <sha>               # imprime os Shorts rascunho
python studio/pipeline/beatgrid.py                  # lista faixas e grades
python studio/pipeline/beatgrid.py "<faixa>.wav"    # estima BPM/fase de uma faixa
python studio/pipeline/imgset.py --train            # dataset de features dos prints + treina
python -m pytest studio/tests/pipeline -q           # testes do pipeline
```

### Dataset de features a partir de prints

`studio/pipeline/imgset.py` transforma imagens paradas em linhas de features —
sem áudio, sem sinais temporais (uma foto não tem os dois): `motion` = 0,
`audio_*` = vazio; o resto (visual + `person_*` + `enemy_*` + `hit_center` +
`friendly_green`) é preenchido.

1. Prints do abate → `frames/kill/`; prints de "nada" → `frames/nada/`
   (ou `--neg-recordings=400` amostra frames chatos das gravações em cache).
2. `python studio/pipeline/imgset.py` → `studio/model/frames_dataset.csv`
   (uma linha por print, dá pra abrir e conferir) + `.npz`.
3. `--train` treina um `HistGradientBoosting` só nesses frames →
   `model/scorer_frames.joblib` + `scorer_frames_meta.json` com o ROC-AUC.

### Notebook

`studio/notebooks/modelo_elementos.ipynb` — com um clipe real do `cache/`:
os 17 sinais base, as 52 features do `derive.augment`, a curva de interesse,
as caixas do YOLO, os frames extremos de cada sinal, combate × caminhada, e no
fim roda `pytest tests/pipeline`. Abra com `jupyter lab` a partir de `studio/`.

O render, a identidade VieirasPlay, a grade do phonk, a mixagem e o `verify`
continuam **inteiramente no harness** (`harness/shorts.py`, `harness/engine.py`).
O studio só escolhe os cortes e dá play nos comandos.

> `harness/shorts.py` foi ajustado (2026-09-09) para aceitar fonte de corte em
> `gravacoes/` além da raiz (linha do "Fonte deve ser uma gameplay...") e para
> contar a numeração `NN_` também em `cliping/*`. Tudo continua preso ao ROOT e
> aos diretórios reservados. O plano agora sai com `output: "cliping/lote<n>"`.
