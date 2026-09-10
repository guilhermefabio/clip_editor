"""Shared paths and analysis constants for the local editing studio.

Everything here is resolved relative to the BODYCAM working folder so the
studio can be launched from any directory, exactly like the harness.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # ...\BODYCAM
HARNESS = ROOT / "harness"
STUDIO = ROOT / "studio"
CACHE = STUDIO / "cache"
MODEL_DIR = STUDIO / "model"
WEB = STUDIO / "web"
GRAVACOES_DIR = ROOT / "gravacoes"     # gravações brutas de gameplay
CLIPING_DIR = ROOT / "cliping"         # saída dos lotes de Shorts renderizados
AUDIO_DIR = ROOT / "audio"             # trilhas (beat_phonk.wav etc.)


def find_source(name: str) -> Path:
    """A recording/clip referenced by a bare filename: look in ``gravacoes/``
    first, then fall back to the BODYCAM root (loose files still work)."""
    n = Path(name).name
    g = GRAVACOES_DIR / n
    return g if g.exists() else ROOT / n


def rel_source(name: str) -> str:
    """ROOT-relative POSIX string for a source, to write into a harness plan
    (``gravacoes/x.mp4`` when it lives there, else the bare name)."""
    p = find_source(name)
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(name).name

FFMPEG = ROOT / "_tools" / "ffmpeg.exe"
FFPROBE = ROOT / "_tools" / "ffprobe.exe"

YOLO_WEIGHTS = MODEL_DIR / "yolov8n.pt"
SCORER_PATH = MODEL_DIR / "scorer.joblib"

# Positives for training: RAW 10-15 s clips cut straight from a recording around
# the kill (no edit, no music). Same domain as the gameplay the model scores,
# gunshot audio intact. The full recordings (via projeto/edicao.json) supply the
# real negatives (walking, menu, loot, dead time).
KILL_CLIPS_DIR = ROOT / "clipes_kill"
KILL_CLIP_MIN_S = 4.0            # ignora clipes curtos demais para ser um kill
KILL_CLIP_MAX_S = 40.0          # e longos demais (provavelmente nao e um clipe de kill)

# Prints (imagens paradas) rotulados por subpasta: frames/kill/ = 1, frames/nada/ = 0.
# Uma foto -> uma linha de features (sem audio, sem sinais temporais).
FRAMES_DIR = ROOT / "frames"

# Kill-marker ROI, as fractions of the frame (x0, y0, x1, y1). Bodycam has no
# on-screen kill feed, only hitmarker ticks dead centre.
KILL_ROI_HITMARKER = (0.44, 0.42, 0.56, 0.58)

# This HUD outlines teammates in green; enemies (the kill targets) have none.
# PROVISIONAL — calibrate the hue range and threshold against a real screenshot
# dropped in studio/model/kill_refs/.
FRIENDLY_GREEN_HSV_LO = (40, 90, 90)      # OpenCV HSV (H 0-179)
FRIENDLY_GREEN_HSV_HI = (85, 255, 255)
FRIENDLY_GREEN_BOX_MIN = 0.05            # fração de verde na borda da caixa p/ ser aliado
FRIENDLY_BOX_PAD = 0.15                  # margem em volta da caixa onde procurar o verde

# Plausibility gate on raw YOLO "person" boxes, applied before they count
# toward person_*/enemy_*. Without it, non-gameplay screens (the in-game
# loadout tablet, matchmaking) get "read" as a giant, low-confidence person
# filling most of the frame — garbage detections that pollute training.
PERSON_MIN_CONF = 0.45          # abaixo disso, ignora a caixa
PERSON_MAX_AREA = 0.55          # caixa/quadro acima disso = tela de menu/tablet, não inimigo

# Legacy alias (rendered-Shorts era). Kept so old imports don't crash.
BEST_SHORTS_DIR = ROOT / "melhores_shorts"

# Frame analysis
FPS_ANALYSIS = 3.0        # sampled frames per second of source
ANALYSIS_WIDTH = 640      # width the source is scaled to before feature work
YOLO_IMGSZ = 480          # inference size for the pretrained detector
YOLO_BATCH = 16
AUDIO_SR = 12000

# Selection defaults. Target short length is 15-20 s; fit_grid picks the actual
# cuts x beats per BPM (was 6 x 8 = 20 s).
DEFAULT_BEATS = 8
DEFAULT_CUTS_PER_SHORT = 6
DEFAULT_MIN_GAP_S = 4.0
CLUSTER_GAP_S = 12.0
# How far (as a multiple of the finished short length) autogroup roams around a
# hot region to pick each cut on its own sub-peak. >1 means dead time (walking,
# reloading) between the sub-peaks is dropped instead of slabbed in.
DEFAULT_SPREAD = 2.2

for _d in (CACHE, MODEL_DIR, GRAVACOES_DIR, KILL_CLIPS_DIR, CLIPING_DIR,
           FRAMES_DIR / "kill", FRAMES_DIR / "nada"):
    _d.mkdir(parents=True, exist_ok=True)
