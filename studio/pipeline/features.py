"""Per-frame feature extraction for a gameplay source.

The source is decoded once through ffmpeg at ``FPS_ANALYSIS`` (uniform sampling,
no seeking), scaled to ``ANALYSIS_WIDTH``. For every sampled frame we compute a
small vector of cheap visual/audio signals plus a few numbers from a pretrained
COCO YOLO detector (enemies on screen). The matrix is cached per source SHA so
training and scoring never re-decode the same file.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402

FEATURE_NAMES = [
    "motion", "center_motion", "brightness", "contrast", "sat_mean",
    "red_frac", "flash_frac", "dark_frac", "edge_density",
    "audio_rms", "audio_hi", "audio_lo",
    "person_count", "person_conf", "person_area", "person_center", "person_area_sum",
    "hit_center", "friendly_green",
    "enemy_count", "enemy_area", "enemy_center",
]
CACHE_VERSION = 7


def _roi_px(roi, w: int, h: int):
    x0, y0, x1, y1 = roi
    return int(x0 * w), int(y0 * h), max(int(x0 * w) + 1, int(x1 * w)), max(int(y0 * h) + 1, int(y1 * h))


from collections import namedtuple  # noqa: E402

_Geom = namedtuple("_Geom", "cx0 cx1 cy0 cy1 hroi glo ghi")


def geom(w: int, h: int) -> "_Geom":
    return _Geom(int(w * .30), int(w * .70), int(h * .22), int(h * .78),
                 _roi_px(C.KILL_ROI_HITMARKER, w, h),
                 np.array(C.FRIENDLY_GREEN_HSV_LO, np.uint8),
                 np.array(C.FRIENDLY_GREEN_HSV_HI, np.uint8))


def visual_row(frame, prev_gray, G: "_Geom"):
    """Fill the non-YOLO, non-audio slots of one feature row from a BGR frame.

    ``motion`` / ``center_motion`` are 0 when ``prev_gray`` is None (a still
    image, or the first video frame). Returns ``(row, gray_float32)`` -- feed the
    gray back as ``prev_gray`` for the next frame.
    """
    import cv2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gf = gray.astype(np.float32)
    if prev_gray is None:
        motion = center_motion = 0.0
    else:
        diff = np.abs(gf - prev_gray)
        motion = float(diff.mean()) / 255.0
        center_motion = float(diff[G.cy0:G.cy1, G.cx0:G.cx1].mean()) / 255.0

    b, gr, r = (frame[:, :, 0].astype(np.int16), frame[:, :, 1].astype(np.int16),
                frame[:, :, 2].astype(np.int16))
    red_frac = float(np.mean((r > 55) & (r > gr * 1.8) & (r > b * 1.8)))
    flash_frac = float(np.mean(gray > 230))
    dark_frac = float(np.mean(gray < 25))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    sat_mean = float(hsv[:, :, 1].mean()) / 255.0
    edges = cv2.Canny(gray, 60, 160)
    edge_density = float(np.mean(edges > 0))
    hx0, hy0, hx1, hy1 = G.hroi
    hit_center = max(0.0, float(np.mean(edges[hy0:hy1, hx0:hx1] > 0)) - edge_density)
    friendly_green = float(np.count_nonzero(cv2.inRange(hsv, G.glo, G.ghi))) / gray.size

    row = np.zeros(len(FEATURE_NAMES), np.float32)
    row[:9] = (motion, center_motion, gray.mean() / 255.0, gray.std() / 128.0,
               sat_mean, red_frac, flash_frac, dark_frac, edge_density)
    row[17:19] = (hit_center, friendly_green)
    return row, gf


def sha256(path: Path) -> str:
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def probe(path: Path) -> dict:
    out = subprocess.check_output(
        [str(C.FFPROBE), "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(path)])
    return json.loads(out)


def source_meta(path: Path) -> dict:
    meta = probe(path)
    v = next(s for s in meta["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {
        "duration": float(meta["format"]["duration"]),
        "width": int(v["width"]),
        "height": int(v["height"]),
        "fps": float(num) / float(den),
        "has_audio": any(s["codec_type"] == "audio" for s in meta["streams"]),
    }


def _decode_frames(path: Path, w: int, h: int, crop: str | None = None):
    """Yield sequential BGR frames sampled at C.FPS_ANALYSIS.

    ``crop`` is an ffmpeg ``crop=`` expression (e.g. ``in_w:in_h*0.75:0:in_h*0.125``)
    applied before the scale -- used to cut the central gameplay band out of a
    rendered 1080x1920 Short, dropping the VieirasPlay overlay.
    """
    vf = f"fps={C.FPS_ANALYSIS}," + (f"crop={crop}," if crop else "") + f"scale={w}:{h}"
    cmd = [str(C.FFMPEG), "-v", "error", "-i", str(path),
           "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=w * h * 3 * 8)
    frame_bytes = w * h * 3
    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    finally:
        proc.stdout.close()
        proc.wait()


def _audio_bands(path: Path, n_frames: int) -> np.ndarray:
    """Return (n_frames, 3) array: rms, high-band, low-band energy per frame."""
    from scipy.signal import butter, sosfilt

    try:
        raw = subprocess.check_output(
            [str(C.FFMPEG), "-v", "error", "-i", str(path),
             "-ac", "1", "-ar", str(C.AUDIO_SR), "-f", "f32le", "-"])
    except subprocess.CalledProcessError:
        return np.zeros((n_frames, 3), np.float32)
    a = np.frombuffer(raw, np.float32)
    if a.size == 0:
        return np.zeros((n_frames, 3), np.float32)
    hi = sosfilt(butter(3, 1800, fs=C.AUDIO_SR, btype="high", output="sos"), a)
    lo = sosfilt(butter(3, 250, fs=C.AUDIO_SR, btype="low", output="sos"), a)
    step = C.AUDIO_SR / C.FPS_ANALYSIS
    out = np.zeros((n_frames, 3), np.float32)
    for i in range(n_frames):
        s = int(i * step)
        e = int(s + step)
        seg_a, seg_h, seg_l = a[s:e], hi[s:e], lo[s:e]
        if seg_a.size:
            out[i] = (np.sqrt(np.mean(seg_a ** 2)),
                      np.sqrt(np.mean(seg_h ** 2)),
                      np.sqrt(np.mean(seg_l ** 2)))
    return out


def _green_ring_frac(bgr, x1, y1, x2, y2) -> float:
    """Fraction of friendly-marker green in a band hugging a person box.

    This HUD outlines teammates in green; enemies have none. Range/threshold in
    :mod:`config` -- PROVISIONAL, calibrate against a real screenshot.
    """
    import cv2

    H, W = bgr.shape[:2]
    pad = int(C.FRIENDLY_BOX_PAD * max(x2 - x1, y2 - y1)) + 1
    ox1, oy1 = max(0, x1 - pad), max(0, y1 - pad)
    ox2, oy2 = min(W, x2 + pad), min(H, y2 + pad)
    crop = bgr[oy1:oy2, ox1:ox2]
    if crop.size == 0:
        return 0.0
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(C.FRIENDLY_GREEN_HSV_LO, np.uint8),
                       np.array(C.FRIENDLY_GREEN_HSV_HI, np.uint8))
    return float(np.count_nonzero(mask)) / mask.size


def _yolo_person_stats(frames: list, model) -> np.ndarray:
    """(len(frames), 8): person count/max_conf/max_area/center_prox/area_sum,
    then **enemy-only** count/max_area/center_prox (person boxes without the
    green friendly outline).

    Boxes failing the plausibility gate (``C.PERSON_MIN_CONF`` /
    ``C.PERSON_MAX_AREA``) are dropped before counting -- the in-game loadout
    tablet and other menu screens otherwise read as one giant, low-confidence
    "person" filling most of the frame.
    """
    import cv2

    rgb = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames]
    res = model.predict(rgb, imgsz=C.YOLO_IMGSZ, verbose=False, classes=[0])
    out = np.zeros((len(frames), 8), np.float32)
    for i, r in enumerate(res):
        b = r.boxes
        if b is None or len(b) == 0:
            continue
        xyxy = b.xyxy.cpu().numpy()
        conf = b.conf.cpu().numpy()
        H, W = r.orig_shape
        areas = ((xyxy[:, 2] - xyxy[:, 0]) * (xyxy[:, 3] - xyxy[:, 1])) / (W * H)
        plausible = (conf >= C.PERSON_MIN_CONF) & (areas <= C.PERSON_MAX_AREA)
        if not plausible.any():
            continue
        xyxy, conf, areas = xyxy[plausible], conf[plausible], areas[plausible]
        cx = (xyxy[:, 0] + xyxy[:, 2]) / 2 / W - 0.5
        cy = (xyxy[:, 1] + xyxy[:, 3]) / 2 / H - 0.5
        dist = np.sqrt(cx ** 2 + cy ** 2)
        green = np.array([_green_ring_frac(frames[i], *box.astype(int)) for box in xyxy])
        enemy = green < C.FRIENDLY_GREEN_BOX_MIN
        e_area = float(areas[enemy].max()) if enemy.any() else 0.0
        e_prox = float(1.0 - dist[enemy].min() / 0.71) if enemy.any() else 0.0
        out[i] = (len(xyxy), float(conf.max()), float(areas.max()),
                  float(1.0 - dist.min() / 0.71), float(areas.sum()),
                  int(enemy.sum()), e_area, e_prox)
    return out


def _align_to_current(X: np.ndarray, names: list) -> tuple[np.ndarray, list]:
    """Line an older cache up with the current FEATURE_NAMES.

    Columns added since the cache was written (e.g. the kill cues) come back as
    NaN -- HistGradientBoosting handles missing values natively, so a recording
    whose source file is gone still contributes its motion/audio/person rows.
    """
    if list(names) == FEATURE_NAMES:
        return X, list(names)
    idx = {n: k for k, n in enumerate(names)}
    out = np.full((X.shape[0], len(FEATURE_NAMES)), np.nan, np.float32)
    for j, n in enumerate(FEATURE_NAMES):
        if n in idx:
            out[:, j] = X[:, idx[n]]
    return out, list(FEATURE_NAMES)


def load_cached(sha: str) -> dict | None:
    """Return the cached feature dict for a SHA, or None if not on disk.

    Lets training survive a deleted source recording. Columns are aligned to the
    current :data:`FEATURE_NAMES`; anything the old cache lacks is NaN.
    """
    npz = C.CACHE / sha / "features.npz"
    if not npz.exists():
        return None
    d = np.load(npz, allow_pickle=True)
    X, names = _align_to_current(d["X"], list(d["names"]))
    return {"times": d["times"], "X": X, "names": names, "sha": sha,
            "version": int(d["version"]) if "version" in d else 0,
            "meta": json.loads(str(d["meta"]))}


def extract(path: Path, progress=None, use_yolo: bool = True,
            crop: str | None = None, cache_tag: str = "") -> dict:
    """Return dict with times, X (N x len(FEATURE_NAMES)), names, sha, meta.

    Cached at ``cache/<sha>/features<cache_tag>.npz``. ``crop`` is an ffmpeg
    ``crop=`` expression applied before scaling (used for rendered Shorts).
    """
    import cv2

    path = Path(path)
    digest = sha256(path)
    cdir = C.CACHE / digest
    cdir.mkdir(parents=True, exist_ok=True)
    npz = cdir / f"features{cache_tag}.npz"
    if npz.exists():
        d = np.load(npz, allow_pickle=True)
        if int(d["version"]) == CACHE_VERSION and bool(d["has_yolo"]) >= use_yolo:
            return {"times": d["times"], "X": d["X"], "names": list(d["names"]),
                    "sha": digest, "meta": json.loads(str(d["meta"]))}

    meta = source_meta(path)
    w = C.ANALYSIS_WIDTH
    h = int(round(w * meta["height"] / meta["width"] / 2) * 2)
    n_est = int(meta["duration"] * C.FPS_ANALYSIS)

    model = None
    if use_yolo:
        try:
            from ultralytics import YOLO
            model = YOLO(str(C.YOLO_WEIGHTS))
        except Exception as exc:  # noqa: BLE001
            print(f"[features] YOLO indisponivel ({exc}); seguindo sem detector.")
            model = None

    G = geom(w, h)
    rows, times = [], []
    prev_gray = None
    batch, batch_idx = [], []

    def flush_yolo(vis_rows):
        if model is None or not batch:
            return
        stats = _yolo_person_stats(batch, model)
        for k, gi in enumerate(batch_idx):
            vis_rows[gi][12:17] = stats[k][:5]      # person_*
            vis_rows[gi][19:22] = stats[k][5:8]     # enemy_*
        batch.clear()
        batch_idx.clear()

    for i, frame in enumerate(_decode_frames(path, w, h, crop)):
        row, prev_gray = visual_row(frame, prev_gray, G)
        rows.append(row)
        times.append(i / C.FPS_ANALYSIS)

        if model is not None:
            batch.append(frame.copy())
            batch_idx.append(len(rows) - 1)
            if len(batch) >= C.YOLO_BATCH:
                flush_yolo(rows)
        if progress and i % 30 == 0 and n_est:
            progress(min(0.99, i / n_est), f"frame {i}/{n_est}")

    if model is not None:
        flush_yolo(rows)

    X = np.vstack(rows).astype(np.float32) if rows else np.zeros((0, len(FEATURE_NAMES)), np.float32)
    times = np.asarray(times, np.float32)
    audio = _audio_bands(path, len(times))
    if len(times):
        X[:, 9:12] = audio

    np.savez_compressed(
        npz, version=CACHE_VERSION, has_yolo=model is not None,
        times=times, X=X, names=np.array(FEATURE_NAMES),
        meta=json.dumps(meta))
    if progress:
        progress(1.0, "features prontas")
    return {"times": times, "X": X, "names": FEATURE_NAMES, "sha": digest, "meta": meta}


if __name__ == "__main__":
    src = Path(sys.argv[1])
    r = extract(src, progress=lambda p, m: print(f"  {p*100:5.1f}%  {m}", end="\r"))
    print()
    print(f"{src.name}: {len(r['times'])} frames, {r['X'].shape[1]} features, sha {r['sha'][:12]}")
    print("means:", dict(zip(r["names"], np.round(r["X"].mean(0), 4))))
