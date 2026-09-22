# Shorts harness — VieirasPlay

This workflow was approved after the user watched Shorts 06–10 in
`shorts_bodycam_lote2/`. It is the persistent reference for requests such as
“I added videos; make five more in our usual style.” Do not reconfirm these
choices for each batch. Explicit user requests may change them.

## Standard delivery

Five distinct videos, normally 20–22 seconds each, exported as MP4/H.264,
1080×1920, 60 fps, yuv420p, stereo AAC at 48 kHz/320 kbps, with faststart.
This preset comes from the approved batch; it is not a YouTube requirement.

Save to a new `shorts_bodycam_loteN/` directory and continue the numbering.
Short 11 was the first number after the approved reference; determine the
current next number from existing files and history. Never overwrite previous
batches. Also deliver the local `ASSISTIR.html` player, cover images,
`projeto/edicao.json`, logs, visual review, and `projeto/verificacao.json`.
The MP4 files are the upload deliverables.

## 1. Inventory and discover new material

Run `python harness/shorts.py inventory`. Inventory accepts root-level
`clipe_*.mp4` recordings; it does not treat `SHORT_*.mp4` exports, previews, or
files inside output directories as new gameplay. For other naming conventions,
include only user-designated sources. Read duration, actual resolution, frame
rate, and audio with FFprobe rather than assuming all recordings match.

Compare SHA-256 hashes, not just filenames or dates. Consult
`harness/historico.json` for hashes and intervals used in previous batches.
An already-used recording may still contain unused moments; a new filename
with an old hash is a copy. Inventory does not mean an entire source is spent.

Since batch 7, root-level `clip_*.mp4` recordings are also accepted. `init`
considers the highest number among existing MP4 files as well as history.
Check archived plans when an earlier batch has not been recorded in history.
Mixed-game batches can specify `game` per Short. Each Short can specify its own
`music`, including hash, BPM, and supporting evidence.

## 2. Select the best moments

Generate contact sheets, initially every 3 seconds, preserving source aspect
ratios. Inspect promising frames every 0.5–1 second and review the seconds
before and after each event. Audio peaks locate candidates; loud gunshots,
death sounds, and voices do not prove kills. Never confirm a kill from volume
or sparse sampling alone.

Prioritize readable encounters, enemies entering the frame, reactions, bursts,
approach, and outcome. Open with nearby action, preferably in the first second.
Remove waiting, menus, respawns, disconnected screens, and long walks. Keep
enough context to understand the encounter. Do not invent kill counts,
victories, clutches, or continuous sequences from unrelated events.

Build five distinct proposals by setting or sequence, normally with 6–7 cuts.
Do not repeat the same encounter across new Shorts or accidentally reuse an
old interval. Repetition within a Short is allowed as a labelled replay. If
strong material is scarce, report that limitation and use available unseen
intervals before artificially stretching weak scenes.

Record each cut's editorial rationale in `note`. The agent prepares the plan
after inspecting the material; the harness itself does not select kills.

## 3. Music and rhythm

Default to `audio/beat_phonk.wav`. The approved track is 30 seconds long with a
**144 BPM** grid; its hash is in `defaults.json`. Verify the hash for each batch.
If the track changes, analyze it and record confirmed BPM and offset in the
plan. Do not blindly reuse 144 BPM: bass autocorrelation was ambiguous for the
reference track; percussion attacks confirmed its grid.

At 144 BPM and 60 fps, one beat equals 25 frames: 4 beats = 1.6667 s,
8 = 3.3333 s, 12 = 5 s, 48 = 20 s, and 52 = 21.6667 s. Prefer blocks of
4, 8, and 12 beats, cutting on attacks while preserving gunshots and outcomes.
At other BPM values, round the grid cumulatively to whole frames.

Vary the music entry point by musical phrase without exceeding the file's
length. Approved entries are 0, 3.3333, 6.6667, and 10 seconds. Preserve pitch
and speed. Do not silently loop or replace the track.

Gameplay normally runs at 1×. Short travel segments may reach approximately
1.4×; replays use 0.65–0.75× and must display `REPLAY / speed`. Use replays only
when warranted, preferably within 20% of the duration. Do not add artificial
shake, strong flashes, or new effects by default.

## 4. Approved presentation

- Vertical canvas: 1080×1920; main gameplay area: 1080×1440 at y=240.
- Main crop width: approximately 0.75×source height. Center the crosshair,
  adjusting `center_x` per cut to include the opponent and outcome. Review
  visually: automatic center cropping can hide the action.
- Background: enlarged, blurred, and darkened source imagery.
- Header: `VIEIRASPLAY` in green `#DAFF64`, a short white title in Portuguese
  for the existing editorial preset, and a small accent line. Keep text outside
  the main gameplay area. Documentation language does not change this preset.
- Footer: setting/theme and `BODYCAM / PHONK`, with a subtle progress indicator.
- Arial Bold fonts; fit titles within 950 px. Defaults: brand y=48/31 px;
  title y=111/up to 53 px; theme y=1711/35 px; footer y=1771/25 px;
  progress y=1840.
- Approved secondary colors: red `#FF765D` and blue `#A7DFFF`.
- Gentle correction: contrast 1.04, brightness 0.006, saturation 1.02,
  gamma 1.08; up to 1.22 in dark tunnels after checking readability.

Adapt cropping to other aspect ratios without stretching. For another FPS
game, change `game` in the plan while retaining the channel identity.

## 5. Mixing and rendering

The preference requested on 2026-09-07 is strong, immersive bass. The
`shorts_bodycam_lote7_bass` revision starts with `audio.music_bass_db: 8`
(a low shelf at 100 Hz, Q 0.707), `music_gain: 0.95`, and `game_gain: 0.62`.
Apply bass boost only to music, inspect each track's result, and retain the
loudness/true-peak limits below. The request updates the bass preference;
it does not establish listening approval of that revision.

Keep gunshots audible and music present. Previously approved starting gains:
gameplay 0.62 and music 0.82; gameplay high-pass at 75 Hz and 3:1 compression;
limiting and final normalization around −14 LUFS. Adapt to the recording;
fixed gain multipliers do not guarantee a good mix.

Render from original sources. Prefer NVIDIA NVENC (the reference machine has
an RTX 4060), H.264 CQ19 intermediates with PCM audio in MKV, and CQ18/preset p5
for the final output. The harness also supports `--encoder libx264`.
Do not concatenate AAC audio from individual cuts: this previously caused
regressing timestamps. Use PCM intermediates, reset timestamps, and quantize
boundaries to frames.

## 6. Required review

`verify` decodes each complete MP4 and checks format, frames, duration, audio
presence, peak, and loudness. Technical acceptance range: −15.5 to −12.5 LUFS,
true peak ≤ −1 dBTP, and no clipping. The target is the approved batch, around
−14 LUFS. Automated validation does not establish editorial quality.

Inspect final contact sheets in `projeto/analise/` and play the videos when a
playback tool is available. Check the opening, opponents, crosshair, text,
dark scenes, encounter outcomes, synchronization, and replays. Do not claim
to have listened or watched in full unless you did. Record the review and any
limitations in `projeto/revisao_editorial.md`.

After review, register the batch with `record`; only then do its intervals
enter history. Deliver links to the player and all five MP4 files. Publishing
to YouTube is a separate action requiring a user request.

## Commands

Run from the repository root. Choose an unused batch/output name for new work;
the following names illustrate the original batch-3 workflow.

```powershell
python harness/shorts.py inventory
python harness/shorts.py init --output shorts_bodycam_lote3 --plan harness/plano_lote3.json
# Inspect the sources, then populate the JSON cuts.
python harness/shorts.py check harness/plano_lote3.json
python harness/shorts.py render harness/plano_lote3.json
python harness/shorts.py verify harness/plano_lote3.json
# Review the result and write projeto/revisao_editorial.md.
python harness/shorts.py record harness/plano_lote3.json
python harness/shorts.py clean harness/plano_lote3.json
```

`clean` removes only that batch's intermediate MKV files after validation and
registration, without recursive deletion. It preserves sources, music,
final outputs, logs, and plans. `render` refuses to overwrite an existing MP4;
use a new output directory for revisions. Do not use historical BAT scripts
to produce a batch in the approved style.

`examples/lote2_aprovado.json` reproduces the approved reference cuts in a
separate directory; it is not a new selection. An initialized plan deliberately
contains empty cuts; the harness requires them to be filled in.

## Public installation and local state

FFmpeg/FFprobe resolve from `_tools/` first, then PATH. See the
[installation guide](../README.md#requirements). Artwork still requires Windows
fonts. CPU rendering: `render <plan> --encoder libx264`.

`plano*.json`, inventory, and history are local state ignored by Git. They were
not deleted during release preparation. Preserve them for numbering and cut
reuse detection. A fresh clone does not contain your production history.
Adapt the [generic plan](../examples/example_plan.json) to your media; the
batch-2 example is historical reference, not a distributed dataset.
`validar_harness.py` depends on that reference's private media.
