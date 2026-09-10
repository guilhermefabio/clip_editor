# studio/youtube — coleta de métricas do YouTube

Subsistema desacoplado que autentica no seu canal, descobre os vídeos, coleta
dados (Data API v3) e performance (Analytics API), e guarda **snapshots
históricos** em SQLite para estudar a curva de crescimento dos Shorts e depois
alimentar modelos de ranking editorial.

Sem LLM. Sem scraping do YouTube Studio.

---

## 1. Projeto no Google Cloud

1. https://console.cloud.google.com → **criar projeto** (ou usar um existente).
2. **APIs e serviços → Biblioteca** → ativar:
   - **YouTube Data API v3**
   - **YouTube Analytics API**
3. **APIs e serviços → Tela de permissão OAuth**:
   - tipo **Externo** (ou Interno se for Workspace);
   - preencher nome do app e e-mail de suporte;
   - **Escopos**: adicionar
     `https://www.googleapis.com/auth/youtube.readonly` e
     `https://www.googleapis.com/auth/yt-analytics.readonly`;
   - em **Usuários de teste**, adicionar o e-mail da conta dona do canal
     (enquanto o app estiver em "Testing", só esses e-mails autenticam e o
     refresh token dura ~7 dias — publique o app para tokens duradouros).
4. **APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth**:
   - tipo de aplicativo **App para computador (Desktop)**;
   - baixar o JSON e salvar como
     `studio/youtube/secrets/client_secret.json`.

## 2. Primeiro refresh token

Numa máquina com navegador:

```powershell
python studio/youtube/auth.py login
```

Abre o consentimento no navegador, grava `secrets/token.json` e imprime o
`refresh_token`. Guarde-o.

## 3. Configurar variáveis

Copie `studio/youtube/.env.example` para `studio/youtube/secrets/youtube.env`
(ou exporte no ambiente):

```
YOUTUBE_CLIENT_ID=...apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...        # o valor impresso no passo 2
YOUTUBE_CHANNEL_ID=             # opcional; vazio = mine=true
```

A pasta `secrets/` está fora de versionamento (`secrets/.gitignore` + `studio/.gitignore`).
Nada de `client_secret` / `access_token` / `refresh_token` vai para log — o
filtro em `log.py` redige.

## 4. Rodar a coleta

```powershell
python studio/youtube/collector.py init                 # cria o schema (metrics.db)
python studio/youtube/collector.py channel              # descobre e grava os vídeos
python studio/youtube/collector.py videos               # lista o que foi gravado
python studio/youtube/collector.py metrics <VIDEO_ID> --window 24h
python studio/youtube/collector.py snapshot --all       # snapshots das janelas devidas
python studio/youtube/collector.py recent --days 45     # canal recente + snapshots
python studio/youtube/collector.py link --apply         # liga Short editado <-> video_id
```

Cada comando é idempotente onde faz sentido (uma janela de idade só é capturada
uma vez; `--force` recaptura). Não abre servidor. Pronto para cron / APScheduler
/ Celery / GitHub Actions — é só chamar o `collector` no horário.

### Janelas por idade do vídeo

`1h, 6h, 24h, 72h, 7d, 28d`. Uma janela só é coletada quando a idade atual do
vídeo está perto do alvo (tolerância em `config.WINDOW_TOLERANCE_HOURS`). Se o
vídeo já passou muito do alvo sem captura, a janela fica **perdida** (a Analytics
é cumulativa até hoje; capturar tarde daria o número errado). Agende a coleta com
frequência suficiente (ex.: de hora em hora nas primeiras 72h).

## 5. Verificar os snapshots

```powershell
python -c "import sys;sys.path.insert(0,'studio');from youtube import storage;c=storage.connect();storage.init_db(c);import json;[print(json.dumps(dict(r),ensure_ascii=False)) for r in c.execute('select video_id,age_window,captured_at,views,engaged_views from youtube_metric_snapshots order by captured_at desc limit 10')]"
```

Ou abra `studio/youtube/metrics.db` em qualquer cliente SQLite.

### Exemplo de registro salvo (`youtube_metric_snapshots`)

```json
{
  "id": 42,
  "video_id": "abc123",
  "captured_at": "2026-09-08T13:00:04Z",
  "video_age_hours": 72.1,
  "age_window": "72h",
  "period_start": "2026-09-05", "period_end": "2026-09-08",
  "views": 1350, "engaged_views": 900,
  "estimated_minutes_watched": 300.0,
  "average_view_duration": 13.8, "average_view_percentage": 62.5,
  "likes": 90, "comments": 10, "shares": 6,
  "subscribers_gained": 22, "subscribers_lost": 3,
  "data_views": 1361, "data_likes": 91, "data_comments": 10,
  "traffic_source": "SHORTS", "creator_content_type": "SHORTS",
  "unavailable_metrics": "",
  "derived_json": {"engaged_view_rate": 0.692, "likes_per_1000_views": 66.7,
                   "subs_per_1000_views": 16.9, "watch_percentage": 0.625},
  "quality_json": {"quality_score": 0.58, "components": {"retention": 0.625, ...}},
  "editor_version": "0.1.0+ab12cd34ef",
  "detector_version": "0.1.0+9f0e1d2c3b",
  "ranking_model_version": "0.1.0+7a6b5c4d3e",
  "render_config_version": "0.1.0+1122334455"
}
```

Snapshots **nunca** são sobrescritos — cada coleta gera uma linha nova. É assim
que se estuda `views 1h → 6h → 24h → 72h`.

## 6. Dataset editorial + YouTube (para o ML depois)

```powershell
python studio/youtube/join.py    # -> studio/youtube/editorial_youtube_dataset.csv
```

Uma linha por Short ligado: `ed_*` (estrutura do `edicao.json` + features
visuais do Short quando há cache) + `yt_*` (métricas por janela 24h/72h/7d +
`yt_growth_24h_72h`) + `target_quality_score` e componentes + os `*_version`.
Serve para regressão / classificação / ranking / séries temporais. O módulo
**não treina** nada — só monta os dados.

### quality_score

Combinação **experimental e configurável** (não é verdade absoluta):

```
quality_score = w1·retention + w2·engaged_view_rate
              + w3·engagement + w4·subscriber_conversion
```

Pesos em `config.QUALITY_WEIGHTS` ou na env `YOUTUBE_QUALITY_WEIGHTS` (JSON).
**Views absolutas não entram** como sinal isolado de qualidade.

## 7. Quota

A API tem um **limite de uso diário** (unidades por projeto), não custo
financeiro. `channels/playlistItems/videos.list` custam ~1 unidade por chamada
(independente do tamanho do lote); a Analytics `reports.query` também é barata.
Uma coleta completa de um canal com centenas de vídeos fica na casa de dezenas
de unidades. Erro `quotaExceeded` vira `QuotaError` e **interrompe** a coleta do
canal (nada mais funcionaria naquele dia) — o resto do estado já persistido fica
intacto.

## Limitações documentadas

- A métrica visual do YouTube Studio **"continuaram assistindo / deslizaram para
  fora"** (swipe-away dos Shorts) **não existe em nenhuma API pública**. Não é
  coletada e não há scraping. Se um dia a API expuser algo equivalente, entra em
  `analytics_api.py`.
- `engagedViews` e o filtro `creatorContentType==SHORTS` só são usados se a API
  responder; contas que não expõem esses identificadores fazem o campo cair para
  `null` (registrado em `unavailable_metrics`).
- Enquanto o app OAuth estiver em "Testing" no Google Cloud, o refresh token
  expira em ~7 dias. Publique o app para tokens duradouros.

## Arquivos

| arquivo | papel |
|---|---|
| `config.py` | env/segredos, janelas de idade, pesos do quality_score |
| `auth.py` | OAuth2 (bootstrap + refresh automático) |
| `client.py` | services Data/Analytics + retry/backoff + erros tipados |
| `data_api.py` | uploads playlist → IDs → `videos.list` em lote |
| `analytics_api.py` | `reports.query` por vídeo/intervalo; segmento SHORTS |
| `features.py` | métricas derivadas + `quality_score` (sem lógica de API) |
| `windows.py` | regra de qual janela coletar agora |
| `storage.py` | SQLite: `youtube_videos`, `youtube_metric_snapshots`, `youtube_short_links` |
| `links.py` | casa Short editado ↔ `video_id` |
| `join.py` | monta a tabela editorial+YouTube para o ML |
| `collector.py` | orquestra tudo + CLI |
| `../versions.py` | carimbo `editor/detector/ranking_model/render_config` |
| `../tests/youtube/` | testes com mock (sem API real) |
