# Harness de Shorts — VieirasPlay

Este é o processo aprovado pelo usuário após assistir aos Shorts 06–10 em
`shorts_bodycam_lote2/`. É a referência persistente para pedidos como
“adicionei vídeos, faça mais cinco no nosso padrão”. Não é necessário reconfirmar
as escolhas abaixo a cada lote. Um pedido novo do usuário pode alterá-las.

## Entrega padrão

Cinco vídeos distintos, normalmente entre 20 e 22 segundos, exportados em
MP4/H.264, 1080×1920, 60 fps, yuv420p, AAC estéreo 48 kHz/320 kbps e faststart.
O padrão vem do lote aprovado; não é apresentado como requisito do YouTube.

Salvar em `shorts_bodycam_loteN/`, com numeração contínua: o próximo lote começa
em **11**. Não sobrescrever os lotes anteriores. Entregar também player local
`ASSISTIR.html`, capas, `projeto/edicao.json`, logs, revisão visual e
`projeto/verificacao.json`. Os MP4 são os arquivos para upload.

## 1. Inventariar e descobrir o material novo

Execute `python harness/shorts.py inventory`. O inventário aceita `clipe_*.mp4`
na raiz; não trata exports `SHORT_*.mp4`, prévias ou arquivos dentro das pastas
de saída como novas gameplays. Se o usuário adotar outros nomes, inclua somente
as fontes indicadas por ele. Leia duração, resolução real, fps e áudio com
FFprobe; não assuma que todas as gravações têm o mesmo tamanho.

Compare SHA-256, não apenas nomes ou datas. Consulte `harness/historico.json`,
que contém hashes e intervalos usados nos lotes anteriores. Uma fonte utilizada
ainda pode ter momentos inéditos; um arquivo novo com hash antigo é uma cópia.
O inventário não significa que uma fonte inteira já foi consumida.

Desde o lote 7, também são aceitas as gravações `clip_*.mp4` adicionadas pelo
usuário na raiz. `init` considera a maior numeração dos MP4 existentes, além
do histórico. Confira também os planos arquivados quando algum lote anterior
ainda não estiver registrado. Lotes mistos podem especificar `game` por Short,
e cada Short pode especificar sua própria `music` com hash, BPM e evidência.

## 2. Selecionar os melhores momentos

Gere folhas de contato, inicialmente a cada 3 s, preservando o aspecto de cada
fonte. Nos candidatos, examine quadros a cada 0,5–1 s e os segundos antes/depois
do evento. Picos de áudio servem para localizar candidatos; tiros altos, ruído
de morte e voz não comprovam abates. Nunca use apenas volume ou amostragem
esparsa para declarar um abate confirmado.

Priorize confrontos legíveis, inimigos entrando em cena, reação, rajadas,
aproximação e desfecho. Abra com ação próxima, de preferência no primeiro
segundo. Corte espera, menus, respawn, telas desconectadas e caminhadas longas.
Preserve contexto suficiente para entender o confronto. Não invente contagem
de kills, vitória, clutch ou sequência contínua a partir de eventos separados.

Monte cinco propostas distintas por cenário ou sequência, normalmente com 6–7
cortes. Não repita o mesmo confronto em dois Shorts novos nem reutilize um
trecho anterior por distração. Repetição dentro do próprio vídeo é permitida
como replay identificado. Se faltar material forte, informe a limitação e use
trechos inéditos disponíveis antes de alongar cenas fracas artificialmente.

Anote o motivo editorial de cada corte em `note`. O plano é criado pelo agente
após olhar o material; o harness não pretende escolher automaticamente as kills.

## 3. Música e ritmo

Usar por padrão `audio/beat_phonk.wav`. O arquivo aprovado tem 30 s e grade
de **144 BPM**; seu hash está em `defaults.json`. Conferir o hash a cada lote.
Se a faixa mudar, analisar o novo áudio e registrar BPM e offset confirmados
no plano. Não herdar 144 BPM cegamente: a autocorrelação dos graves deste beat
deu uma estimativa ambígua; os ataques da percussão confirmaram 144 BPM.

A 144 BPM e 60 fps: 1 beat = 25 quadros; 4 = 1,6667 s; 8 = 3,3333 s;
12 = 5 s; 48 = 20 s; 52 = 21,6667 s. Preferir blocos de 4, 8 e 12 beats,
com mudança de cena nos ataques e preservação do tiro/desfecho. A grade é
arredondada cumulativamente para quadros inteiros quando o BPM for diferente.

Variar a posição de entrada da música em frases musicais, sem ultrapassar a
duração do arquivo. Entradas aprovadas: 0, 3,3333, 6,6667 e 10 s. Preservar a
velocidade e afinação da faixa. Não fazer loop ou trocar o beat silenciosamente.

Gameplay normalmente em 1×. Acelerar deslocamentos curtos até aproximadamente
1,4×; replay em 0,65–0,75×, sempre marcado `REPLAY / velocidade`. Usar replay
apenas quando o momento justificar, preferencialmente até 20% da duração.
Não adicionar tremor artificial, flashes fortes ou efeitos novos por padrão.

## 4. Aparência aprovada

- Tela vertical 1080×1920; gameplay principal 1080×1440, em y=240.
- Recorte principal com largura aproximada de 0,75×altura da fonte; centralizar
  a mira, ajustando `center_x` por corte para incluir o adversário e o desfecho.
  Conferir visualmente: um recorte central automático pode esconder a ação.
- Fundo derivado da própria imagem, ampliado, desfocado e escurecido.
- Topo: `VIEIRASPLAY` em verde `#DAFF64`, título branco curto em português,
  pequeno traço na cor do vídeo; textos fora da área principal de gameplay.
- Rodapé: cenário/tema e `BODYCAM / PHONK`, com indicador discreto de progresso.
- Fontes Arial Bold, títulos ajustados para caber em até 950 px. Defaults:
  marca y=48/31 px; título y=111/até 53 px; tema y=1711/35 px;
  rodapé y=1771/25 px; progresso y=1840.
- Cores secundárias aprovadas: vermelho `#FF765D` e azul `#A7DFFF`.
- Correção suave: contraste 1,04, brilho 0,006, saturação 1,02, gamma 1,08;
  nos túneis escuros, até 1,22 após conferir que a ação ficou legível.

Se a origem tiver outro aspecto, adapte o recorte sem esticar as proporções.
Se for outro jogo FPS, altere `game` no plano e mantenha a identidade do canal.

## 5. Mixagem e renderização

Preferência solicitada em 07/09/2026: música com bass alto e envolvente.
Na revisão `shorts_bodycam_lote7_bass`, o ponto de partida é
`audio.music_bass_db: 8` (low shelf em 100 Hz, Q 0,707), `music_gain: 0.95`
e `game_gain: 0.62`. Aplicar o reforço apenas à música, conferir o resultado
para cada beat e manter os limites de loudness/true peak abaixo. Este pedido
atualiza a preferência de graves; não representa aprovação auditiva da revisão.

Manter os tiros audíveis e a música presente. Valores iniciais aprovados:
gameplay 0,62, beat 0,82; high-pass de 75 Hz e compressor 3:1 no jogo;
limitador e normalização final para cerca de −14 LUFS. Ajustar se a captura
exigir, sem tratar multiplicadores fixos como garantia de uma boa mixagem.

Usar os arquivos originais na renderização final. Preferir NVIDIA NVENC
(máquina aprovada: RTX 4060), intermediários H.264 CQ19 e PCM em MKV;
final CQ18/preset p5. Há alternativa `--encoder libx264` no harness.
Não concatenar áudio AAC de cada corte: isso já causou timestamps regressivos.
Usar PCM nos intermediários, timestamps reiniciados e quantização por quadro.

## 6. Revisão obrigatória

`verify` decodifica cada MP4 inteiro e verifica formato, frames, duração,
presença de áudio, pico e loudness. Faixa técnica de aceite: −15,5 a −12,5 LUFS,
true peak ≤ −1 dBTP, áudio sem clipping. O alvo é o lote aprovado, em torno
de −14 LUFS. A revisão automatizada não comprova que os cortes são os melhores.

Inspecione as folhas finais em `projeto/analise/` e reproduza os vídeos quando
houver ferramenta de reprodução disponível. Confira abertura, adversários,
mira, textos, cenas escuras, fim de cada confronto, sincronização e replays.
Não afirme ter ouvido ou assistido integralmente sem fazê-lo. Registre a revisão
em `projeto/revisao_editorial.md`, incluindo qualquer limitação de revisão.

Concluída a revisão, registre o lote com `record`. Somente então os intervalos
entram no histórico. Entregar links para o player e os cinco MP4. Publicação no
YouTube é uma ação separada e depende de pedido do usuário.

## Comandos

Executar a partir da pasta BODYCAM:

```powershell
python harness/shorts.py inventory
python harness/shorts.py init --output shorts_bodycam_lote3 --plan harness/plano_lote3.json
# O agente preenche os cortes no JSON após inspecionar as fontes.
python harness/shorts.py check harness/plano_lote3.json
python harness/shorts.py render harness/plano_lote3.json
python harness/shorts.py verify harness/plano_lote3.json
# O agente inspeciona a revisão e escreve projeto/revisao_editorial.md.
python harness/shorts.py record harness/plano_lote3.json
python harness/shorts.py clean harness/plano_lote3.json
```

`clean` remove apenas os intermediários MKV deste lote, depois da validação e
registro, sem remoção recursiva. Não altera fontes, música, finais, logs ou planos.
`render` recusa sobrescrever um MP4 existente: para uma revisão, use uma nova
pasta de saída. Não execute os BAT históricos para produzir um lote no padrão.

`examples/lote2_aprovado.json` reproduz os cortes de referência em uma pasta
separada; não é uma seleção nova. O plano `plano_lote3.json` fica como ponto
de partida, com cortes vazios de propósito. O harness exige que sejam preenchidos.
