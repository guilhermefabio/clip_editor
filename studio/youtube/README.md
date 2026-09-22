# studio/youtube — YouTube metrics collection

An optional, separate subsystem that authenticates with your channel,
discovers videos, collects metadata through Data API v3 and performance through
Analytics API, and stores **historical snapshots** in SQLite. The data supports
studying Shorts growth and preparing future editorial ranking models.

No LLM is used, and the collector does not scrape YouTube Studio.

## 1. Google Cloud project

Create or select a project in the [Google Cloud console](https://console.cloud.google.com/).
Enable **YouTube Data API v3** and **YouTube Analytics API** in the API library.
Configure the OAuth consent screen with the application name, support email,
and appropriate audience for your account. Add the following scopes:

- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

For a testing configuration, add the channel owner's account as a test user.
Testing-mode refresh tokens may expire; check the applicable consent-screen
settings and Google policies before relying on unattended collection.

Create an OAuth client of type **Desktop app**, download its JSON, and store
it locally at `studio/youtube/secrets/client_secret.json`.

## 2. Obtain the first refresh token

On a machine with a browser, run:

```powershell
python studio/youtube/auth.py login
```

The command opens the browser consent flow, saves `secrets/token.json`, and
prints the refresh token to the terminal. Keep that value private; do not
include the terminal output in public logs or screenshots. The saved token
file can be used directly instead of copying the token into an environment file.

## 3. Configure credentials

Copy `studio/youtube/.env.example` to
`studio/youtube/secrets/youtube.env`, or set environment variables:

```dotenv
YOUTUBE_CLIENT_ID=...apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
YOUTUBE_CHANNEL_ID=
```

The channel ID is optional; an empty value uses `mine=true`. Credential lookup
supports environment variables, the local environment file, and the Google
credential/token files documented in `config.py` and `auth.py`.

The secrets directory is ignored through its own `.gitignore` and
`studio/.gitignore`. The application logger redacts configured secret fields;
the interactive login's explicit terminal output must still be handled privately.
Never commit OAuth files, tokens, or feedback databases.

## 4. Run collection

```powershell
python studio/youtube/collector.py init                 # Create metrics.db schema
python studio/youtube/collector.py channel              # Discover and store videos
python studio/youtube/collector.py videos               # List stored videos
python studio/youtube/collector.py metrics <VIDEO_ID> --window 24h
python studio/youtube/collector.py snapshot --all        # Collect currently due windows
python studio/youtube/collector.py recent --days 45      # Recent channel videos and snapshots
python studio/youtube/collector.py link --apply          # Link edited Shorts to video IDs
```

Commands avoid duplicate collection where applicable: an age window is
normally captured once, while `--force` requests another capture. The collector
does not run a persistent server or scheduler. Invoke it from your own scheduler
if recurring collection is required, keeping credentials and the database private.

### Video-age windows

Configured windows are `1h`, `6h`, `24h`, `72h`, `7d`, and `28d`. A window is
collected only when the video's current age is close enough to the target;
tolerances live in `config.WINDOW_TOLERANCE_HOURS`. If collection misses that
range, the window remains missing rather than labelling a later cumulative
measurement as the earlier one. Schedule frequently enough for the intended
windows, for example hourly during the first 72 hours. Reporting latency can
still limit how useful early snapshots are.

## 5. Inspect snapshots

```powershell
python -c "import sys;sys.path.insert(0,'studio');from youtube import storage;c=storage.connect();storage.init_db(c);import json;[print(json.dumps(dict(r),ensure_ascii=False)) for r in c.execute('select video_id,age_window,captured_at,views,engaged_views from youtube_metric_snapshots order by captured_at desc limit 10')]"
```

Alternatively, open `studio/youtube/metrics.db` with a SQLite client.

### Illustrative snapshot

The following values illustrate `youtube_metric_snapshots`; they are not
measured project results. Derived/quality fields are shown as decoded objects
for readability.

```json
{
  "id": 42,
  "video_id": "example_video_id",
  "captured_at": "2026-09-08T13:00:04Z",
  "video_age_hours": 72.1,
  "age_window": "72h",
  "period_start": "2026-09-05",
  "period_end": "2026-09-08",
  "views": 1350,
  "engaged_views": 900,
  "estimated_minutes_watched": 300.0,
  "average_view_duration": 13.8,
  "average_view_percentage": 62.5,
  "likes": 90,
  "comments": 10,
  "shares": 6,
  "subscribers_gained": 22,
  "subscribers_lost": 3,
  "data_views": 1361,
  "data_likes": 91,
  "data_comments": 10,
  "traffic_source": "SHORTS",
  "creator_content_type": "SHORTS",
  "unavailable_metrics": "",
  "derived_json": {
    "engaged_view_rate": 0.667,
    "likes_per_1000_views": 66.7,
    "subs_per_1000_views": 16.3,
    "watch_percentage": 0.625
  },
  "quality_json": {
    "quality_score": 0.58,
    "components": {"retention": 0.625}
  },
  "editor_version": "0.1.0+ab12cd34ef",
  "detector_version": "0.1.0+9f0e1d2c3b",
  "ranking_model_version": "0.1.0+7a6b5c4d3e",
  "render_config_version": "0.1.0+1122334455"
}
```

Snapshots are historical records: a new capture creates a new row instead of
overwriting the earlier snapshot. This supports comparing growth across ages.

## 6. Editorial and YouTube dataset

```powershell
python studio/youtube/join.py
# Writes studio/youtube/editorial_youtube_dataset.csv
```

The output has one row per linked Short: `ed_*` features from `edicao.json`
and cached visual features where available, `yt_*` metrics for 24h/72h/7d,
`yt_growth_24h_72h`, `target_quality_score`, score components, and version tags.
The table is intended for future regression, classification, ranking, or time
series experiments. This module assembles data; it **does not train a model**.

### Quality score

The quality score is an **experimental, configurable** combination, not an
objective ground-truth definition of quality:

```text
quality_score = w1 * retention + w2 * engaged_view_rate
              + w3 * engagement + w4 * subscriber_conversion
```

Weights are in `config.QUALITY_WEIGHTS` or the JSON environment variable
`YOUTUBE_QUALITY_WEIGHTS`. Absolute views are not used as a standalone quality
signal. Inspect feature definitions and missing-data handling before using the
score as a training target.

## 7. Quota handling

Collection consumes API quota. Check the quota allocation and method costs
for your Google Cloud project before scheduling large jobs. The client uses
batched metadata requests where supported. A `quotaExceeded` response becomes
`QuotaError` and stops channel collection; state already persisted remains
intact. A completed local batch does not guarantee further quota is available.

## Limitations

- The collector does not collect the YouTube Studio “viewed versus swiped away”
  metric or scrape the Studio interface. Any future API equivalent would need
  an explicit implementation in `analytics_api.py`.
- `engagedViews` and the `creatorContentType==SHORTS` filter are used when
  supported by the API response. Unsupported fields are represented as `null`
  and recorded in `unavailable_metrics` rather than fabricated.
- OAuth testing configuration can limit refresh-token lifetime. Expired or
  revoked credentials require renewed authorization; configure OAuth for your
  intended deployment rather than assuming a token will remain valid forever.
- Snapshot timing and reporting availability affect comparability. Missing
  windows should remain explicit when building later ranking datasets.

## Files

| File | Role |
| --- | --- |
| `config.py` | Credentials, age windows, and quality-score weights. |
| `auth.py` | OAuth bootstrap and automatic refresh. |
| `client.py` | Data/Analytics services, retry/backoff, and typed errors. |
| `data_api.py` | Upload playlist discovery and batched video metadata. |
| `analytics_api.py` | Per-video/date-range reports and Shorts segmentation. |
| `features.py` | Derived metrics and quality score, separate from API calls. |
| `windows.py` | Decide which age window is currently due. |
| `storage.py` | SQLite videos, metric snapshots, and Short links. |
| `links.py` | Match edited Shorts to YouTube video IDs. |
| `join.py` | Build the editorial/YouTube dataset. |
| `collector.py` | Collection orchestration and CLI. |
| `../versions.py` | Editor, detector, ranking-model, and render-config version tags. |
| `../tests/youtube/` | Mocked tests without live API access. |
