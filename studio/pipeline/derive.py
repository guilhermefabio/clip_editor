"""Turn the raw per-frame feature matrix into the vector the scorer sees.

Keeps the on-disk cache raw so these derived signals can be tuned without
re-decoding video. "Interesting" is a temporal notion, so every base signal
gains a short windowed max and mean (roughly +/- 1.5 s).
"""
from __future__ import annotations

import numpy as np

WINDOW_COLS = [
    "motion", "center_motion", "flash_frac", "red_frac", "contrast",
    "audio_rms", "audio_hi", "audio_lo",
    "person_count", "person_conf", "person_area", "person_center", "person_area_sum",
    "hit_center", "friendly_green",
    "enemy_count", "enemy_area", "enemy_center",
]

# Signals whose *spike above the surrounding seconds* marks a firefight (or a
# kill). Walking has steady global motion but none of these jump, so the gap
# between the two is what separates real combat from "still moving, nothing".
SPIKE_COLS = [
    "flash_frac", "red_frac", "audio_hi", "audio_lo",
    "person_area", "person_area_sum", "center_motion",
    "hit_center", "enemy_area", "enemy_count",
]


def _rolling(a: np.ndarray, half: int, fn) -> np.ndarray:
    n = len(a)
    if n and np.isnan(a).all():        # coluna ausente num cache antigo
        return np.full(n, np.nan, np.float32)
    out = np.empty(n, np.float32)
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        out[i] = fn(a[lo:hi])
    return out


def augment(times: np.ndarray, X: np.ndarray, names: list, fps: float = 3.0):
    if X.shape[0] == 0:
        return X, list(names)
    half = max(1, int(round(1.5 * fps)))
    idx = {n: k for k, n in enumerate(names)}
    cols = [X]
    new_names = list(names)
    for name in WINDOW_COLS:
        if name not in idx:
            continue
        col = X[:, idx[name]]
        wmax = _rolling(col, half, np.max)
        wmean = _rolling(col, half, np.mean)
        cols.append(np.column_stack([wmax, wmean]))
        new_names += [f"{name}_wmax", f"{name}_wmean"]
    # spike above the local baseline (~+/- 4 s): value now minus its own
    # surrounding mean, floored at 0. A firefight spikes these; walking doesn't.
    base_half = half * 3
    for name in SPIKE_COLS:
        if name not in idx:
            continue
        col = X[:, idx[name]]
        spike = np.maximum(0.0, col - _rolling(col, base_half, np.mean))
        cols.append(spike[:, None])
        new_names.append(f"{name}_spike")
    # crude "is this a menu / dead time" flag: sustained low motion + low audio
    if "center_motion" in idx and "audio_rms" in idx:
        cm = _rolling(X[:, idx["center_motion"]], half * 2, np.mean)
        ar = _rolling(X[:, idx["audio_rms"]], half * 2, np.mean)
        idle = ((cm < 0.02) & (ar < 0.01)).astype(np.float32)
        cols.append(idle[:, None])
        new_names.append("idle_flag")
    # "walking" cue: global motion well above this clip's own median while none
    # of the combat spikes fire nearby -- steady travel, nothing happening.
    if "motion" in idx:
        mv = _rolling(X[:, idx["motion"]], base_half, np.mean)
        fl = _rolling(X[:, idx["flash_frac"]], base_half, np.max) if "flash_frac" in idx else np.zeros(len(mv), np.float32)
        hi = _rolling(X[:, idx["audio_hi"]], base_half, np.max) if "audio_hi" in idx else np.zeros(len(mv), np.float32)
        moving = mv > max(1e-6, float(np.median(mv)))
        quiet = (fl <= np.quantile(fl, 0.4)) & (hi <= np.quantile(hi, 0.4))
        walk = (moving & quiet).astype(np.float32)
        cols.append(walk[:, None])
        new_names.append("walk_flag")
    return np.hstack(cols).astype(np.float32), new_names
