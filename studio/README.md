# BODYCAM Studio

A **local** web interface that analyzes gameplay recordings, suggests moments
of interest using a model trained on approved edits, assembles Shorts in the
VieirasPlay preset, and renders through the existing harness.

No LLM is used. You enter each Short's title, theme, and name. The model
suggests where interesting moments may occur; editorial review is still needed.

The optional [YouTube feedback collector](youtube/README.md) uses OAuth 2.0,
Data API v3 and Analytics API, with historical snapshots in SQLite. Its CLI is
`python studio/youtube/collector.py`.

## 1. Run the Studio

```powershell
# From the repository root, after activating your virtual environment:
python -m pip install -r studio/requirements.txt
python studio/app.py
```

Open **http://127.0.0.1:8765**. This is a localhost server without authentication.
Weight downloads and the optional YouTube integration may access the network.
Stop it with `Ctrl+C` in the terminal.

### Directories

| Directory | Contents |
| --- | --- |
| `gravacoes/` | Raw `.mkv`/`.mp4` gameplay for analysis and training negatives. Root-level source files are also supported. |
| `clipes_kill/` | Raw kill clips, typically 10–15 seconds, used as positive training examples. |
| `frames/kill/`, `frames/nada/` | Labelled positive/negative stills. One image becomes one feature row through `pipeline/imgset.py`. |
| `cliping/lote<n>/` | Rendered Shorts and `projeto/edicao.json`. Older batches may use `shorts_bodycam*/`. |
| `studio/model/kill_refs/` | Reference screenshots for ROI and friendly-HUD calibration. |

Install all dependencies in a virtual environment; see the
[installation guide](../README.md#requirements). Windows/Python 3.13 is the
tested environment. FFmpeg/FFprobe are found in `_tools/` first, then PATH.
YOLO weights, a fitted scorer, datasets, and music are not included in a clone.
Read [dataset provenance](../docs/DATASET.md) before training.

## 2. Editing workflow

The current application interface uses Portuguese labels. The workflow below
describes the controls in English; documentation translation does not change
the application UI or filesystem names.

In the source section, add two or more recordings to the merge control, order
them with the arrow buttons, and start merging. The merged file becomes the
selected source. Analyze it to continue. Short videos are also listed.

Merging creates `gravacoes/unidos_<id>.mp4` and an `.origens.json` mapping,
preserving originals. Gameplay audio is retained; silent segments receive
silence. Resolution and frame rate follow the first recording, capped at
60 fps, with padding rather than stretching. H.264 re-encoding can take time
for long recordings. Identical content is rejected by SHA-256. Rendering plans
map cuts back to original files/timestamps so history tracks their sources.
A cut crossing a join boundary requires a timeline adjustment.

| Step | Section | Action |
| --- | --- | --- |
| 1 | Source | Select a recording from `gravacoes/` or the root and analyze it. Results are cached in `studio/cache/<sha>/`. Runtime depends on source length and hardware. |
| 2 | Interest curve | Inspect the green score curve, red threshold, and blue candidates. Click to preview a frame. Set batch size, cuts per Short, spread, audio track, and entry beat, then group automatically. Higher spread searches farther around each region for separate action peaks. |
| 3 | Shorts | Review each peak thumbnail; edit name, title, theme/tag, color, beats per cut, and per-Short music/entry overrides. Nudge cuts by ±0.5 s, preview, remove, add, or mark replays. Duration is green at 20–22 s and red outside that range. |
| 4 | Generate plan | Save `harness/plano_<batch>.json` and run harness `check`. Rendering becomes available only after validation succeeds. |
| 5 | Render | Run `shorts.py render`, followed by `verify`, with progress and live logs. |
| 6 | Review | Inspect final MP4 files, thumbnails, measured LUFS, and the batch's `ASSISTIR.html` player. |

## 3. Audio tracks and beat grids

The selector lists `.wav`/`.mp3` files in `audio/`, plus root-level files for
backward compatibility. Tracks with a confirmed BPM and grid offset in
`defaults.json` or an approved plan can reuse that grid. Historical local
examples are shown below; the audio files are not distributed.

| File | BPM | Grid offset |
| --- | --- | --- |
| `beat_phonk.wav` | 144 | 0 s |
| `bodycam_hook_dark_phonk.wav` | 140 | 0.045 s |
| `slow_dark_russian_phonk.mp3` | 130 | 0.917 s |
| `slow_dark_russian_phonk1.mp3` | 148 | 1.217 s |

For an unknown grid, use beat analysis. It estimates BPM/phase from the
percussion envelope above 1800 Hz and offers candidates. Choose one after
review; evidence is saved in the plan. The harness rejects tracks without
grid evidence.

Music entry is `grid_offset + n * 60 / BPM`, keeping it on a beat. If an entry
would extend beyond the track, it moves backward in four-beat increments.
Cut duration follows `beats * 60 / BPM`: six eight-beat cuts total 20 seconds
only at 144 BPM. `fit_grid` chooses a cut count and beat count to fit 20–22 s.

| BPM | Example grid | Total |
| --- | --- | --- |
| 144 | 6 × 8 beats | 20.00 s |
| 140 | 6 × 8 beats | 20.57 s |
| 130 | 5 × 9 beats | 20.77 s |
| 148 | 6 × 9 beats | 21.89 s |

Each Short can override its track and entry point.

## 4. Interest model

Pretrained COCO `yolov8n` supplies person count, confidence, area, center, and
summed-area features. Before counting, bounding boxes pass plausibility filters
(`PERSON_MIN_CONF`, `PERSON_MAX_AREA` in `config.py`) to reduce large false
person detections on menus/loadout screens. Remaining boxes are classified by
the green friendly-HUD outline heuristic, producing `enemy_count`,
`enemy_area`, and `enemy_center`. These are imperfect cues, not verified kills.

At **3 FPS**, the pipeline also extracts global/central motion, brightness,
contrast, saturation, red/flash/dark fractions, edge density, friendly-green
coverage, RMS/high/low audio bands, and the central hitmarker signal
`hit_center`. The current HUD implementation uses central marker cues rather
than a kill-feed ROI.

`derive.py` adds windowed maxima/means over approximately ±1.5 s, spikes above
a local baseline of roughly ±4 s, and `idle_flag`/`walk_flag`: **70 features**
in total. Combat-related spikes help locate candidates but do not prove kills.

The scorer is scikit-learn's `HistGradientBoostingClassifier`. Training uses
raw gameplay, not rendered Shorts or added music. Positives include approved
source intervals, raw kill-clip frames, and reviewed positive stills. Negatives
come from outside approved intervals or reviewed negative stills. Missing
features can remain `NaN`. `--raw-only` excludes kill clips and reviewed stills,
using recordings with approved cuts only. ROI and friendly-green settings
remain provisional and require calibration against suitable screenshots.

`group.py` detects peaks in the smoothed curve and groups nearby candidates
with a 12-second cluster gap. Within a region spanning spread × Short length
(default spread 2.2×), it seeks separate sub-peaks and orders cuts chronologically,
removing travel/reload gaps where possible. When insufficient distinct peaks
exist, it falls back to a contiguous region. Spread 1× approximates the older
contiguous behavior. Proposed cuts across different Shorts avoid overlap.

### Model panel

The panel reads `studio/model/scorer_meta.json` and displays:

- ROC-AUC and Average Precision from the saved validation report. New runs use
  recording-disjoint validation with at least two known origins; unknown origins
  are excluded from validation.
- Precision, recall, and F1. New runs use a fixed evaluation threshold of 0.5;
  the operational suggested threshold is separate. Metrics tuned and measured
  on the same OOF predictions are optimistic diagnostics.
- Positive/negative counts, feature count, source count, and analysis FPS.
- Training-source details, including cached-only sources.
- Permutation importance bars, which are descriptive training-data statistics.

Use the train/retrain control or `python studio/pipeline/train.py` to fit a model.
This writes local model artifacts. Feature caches can supply recording rows
when the original file is missing. Metadata includes `raw_only`, `source`,
`n_kill_clips`, and `audio_used`.

Earlier experiments trained on rendered Shorts with too few negatives and
without gameplay audio. The main scorer now uses raw gameplay and reviewed
stills; the limitations of this supervision remain documented in the
[model card](../MODEL_CARD.md).

## 5. Experimental status

Read the [model card](../MODEL_CARD.md) for historical metrics, validation
limitations, and the difference between old results and the revised evaluator.
Old machine/session notes are preserved locally in ignored `legacy/local/`;
they do not describe a fresh installation. Supply training data and fit a model
locally before using scoring features.

YOLO is a pretrained feature extractor. Cuts still need visual and editorial
review. The interface has no undo/redo; reloading loses transient page state
while retaining disk caches.

## 6. Files

| Path under `studio/` | Role |
| --- | --- |
| `config.py` | Paths, analysis constants, ROI and friendly-HUD settings. |
| `pipeline/features.py` | FFmpeg decoding and 22 base signals cached in `cache/<sha>/features.npz`. |
| `pipeline/derive.py` | Temporal windows, spikes, idle/walking flags; 70 total features. |
| `pipeline/dataset.py` | Training rows from raw clips, approved recording intervals, and reviewed stills. |
| `pipeline/imgset.py` | Still-image feature datasets and a separate experimental image scorer. |
| `pipeline/train.py` | Fit/evaluate the main scorer; save `model/scorer.joblib` and `scorer_meta.json`. |
| `pipeline/score.py` | Apply the scorer and cache interest curves. |
| `pipeline/group.py` | Peaks, candidates, draft Shorts, `fit_grid`, and `music_start_for`. |
| `pipeline/beatgrid.py` | Track registry and BPM/phase estimation. |
| `pipeline/planbuild.py` | Write harness plans and run `check`. |
| `pipeline/media.py` | Extract preview frames. |
| `app.py` | FastAPI server and API. |
| `web/index.html`, `web/app.js` | Single-page editing interface. |
| `model/` | Local YOLO weights, trained scorers, and metadata. |
| `cache/<sha>/` | Source features, scores, and frames; `sources.json` indexes sources. |
| `model/kill_refs/` | ROI/HUD calibration screenshots. |
| `tests/pipeline/` | Pipeline regression tests. |
| `notebooks/modelo_elementos.ipynb` | Exploratory feature/model notebook using local data. |

### CLI equivalents

```powershell
python studio/pipeline/features.py "<video>"       # Extract features
python studio/pipeline/train.py                    # Train the scorer
python studio/pipeline/score.py "<video>"          # Generate an interest curve
python studio/pipeline/group.py <sha>              # Print draft Shorts
python studio/pipeline/beatgrid.py                 # List tracks and grids
python studio/pipeline/beatgrid.py "<track>.wav"   # Estimate BPM/phase
python studio/pipeline/imgset.py --train           # Train the separate image experiment
python -m pytest studio/tests/pipeline -q          # Run pipeline tests
```

### Still-image feature dataset

`pipeline/imgset.py` converts labelled stills to feature rows. A still has no
audio or inter-frame motion: motion is zero and audio fields are missing;
visual, person, enemy, hitmarker, and friendly-green signals are extracted.

1. Place positive stills in `frames/kill/` and negatives in `frames/nada/`.
   `--neg-recordings=400` can sample negative frames from cached recordings.
2. Run `python studio/pipeline/imgset.py` to create local
   `studio/model/frames_dataset.csv` and `.npz` files.
3. `--train` fits a separate `HistGradientBoosting` image model and writes
   `model/scorer_frames.joblib` and `scorer_frames_meta.json`. Its evaluation
   is separate from the revised main scorer; do not conflate their metrics.

### Notebook and rendering boundary

`notebooks/modelo_elementos.ipynb` illustrates signals, YOLO boxes, extreme
frames, combat versus walking, and interest curves using local cached media.
It also includes test and optional training cells. Open JupyterLab from
`studio/` and inspect training controls before running all cells. Public
notebook outputs are cleared; the notebook itself is not a bundled dataset.

Rendering, VieirasPlay artwork, beat synchronization, mixing, and `verify`
remain in `harness/shorts.py` and `harness/engine.py`. Studio prepares cuts and
invokes those commands. The harness accepts `gravacoes/` sources and counts
numbered outputs under `cliping/*`; generated plans use `cliping/lote<n>`.
Paths remain constrained to the workspace and its reserved-directory rules.
