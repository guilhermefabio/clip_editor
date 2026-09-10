"""Peak-pick the interest curve and auto-assemble draft shorts.

The output plan lands each short in 15-20 s on the beat grid of the track
(``fit_grid`` picks cuts/beats per BPM). Each short's cuts are picked on
*separate* sub-peaks inside a hot
region, so walking / reloading between them is dropped instead of slabbed in --
the way the hand-made lotes were cut. Everything here is a starting point the
user rearranges in the web UI; title, tag and name are left blank on purpose.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy.signal import find_peaks

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402

BPM = 144.0
LEAD_FRAC = 0.35        # a picked sub-peak sits ~35 % into its own cut


def next_short_number() -> int:
    nums = []
    hist_path = C.HARNESS / "historico.json"
    if hist_path.exists():
        hist = json.loads(hist_path.read_text(encoding="utf-8-sig"))
        for b in hist.get("batches", []):
            for s in b.get("shorts", []):
                m = re.match(r"^(\d+)", s)
                if m:
                    nums.append(int(m.group(1)))
    for folder in C.ROOT.glob("shorts_*"):
        if folder.is_dir():
            for p in folder.glob("*.mp4"):
                m = re.match(r"^(\d+)_", p.name)
                if m:
                    nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def candidates(score: dict, min_gap_s: float = C.DEFAULT_MIN_GAP_S, limit: int = 60) -> list[dict]:
    t = np.asarray(score["times"], float)
    s = np.asarray(score["smooth"], float)
    if len(s) == 0:
        return []
    fps = score["fps_analysis"]
    prom = max(0.04, 0.6 * float(s.std()))
    height = min(0.35, 0.6 * score["threshold"])
    idx, props = find_peaks(s, distance=max(1, int(min_gap_s * fps)),
                            prominence=prom, height=height)
    cand = [{"t": round(float(t[i]), 2), "score": round(float(s[i]), 4)} for i in idx]
    cand.sort(key=lambda c: c["score"], reverse=True)
    cand = cand[:limit]
    cand.sort(key=lambda c: c["t"])
    return cand


def _cut(file: str, start: float, dur_source: float, cd: float, beats: float, note: str) -> dict:
    start = max(0.0, min(start, dur_source - cd - 0.05))
    return {"file": file, "start": round(start, 3), "beats": beats,
            "speed": 1, "center_x": 0.5, "gamma": 1.1, "replay": False, "note": note}


def resolve_music(music: dict | None) -> dict:
    """Fill in file/sha/bpm/grid/evidence/duration for the chosen track."""
    m = dict(music) if music else _default_music()
    if "duration" not in m or not m["duration"]:
        from pipeline import beatgrid
        m["duration"] = round(beatgrid._duration(C.ROOT / m["file"]), 2)
    m.setdefault("grid_offset_seconds", 0.0)
    return m


def fit_grid(bpm: float, want_cuts: int, dur_range=(15.0, 20.0)) -> tuple[int, float, float]:
    """Pick (cuts, beats_per_cut, cut_seconds) so the short lands in dur_range
    on the beat grid of this BPM. Prefers the requested cut count and blocks of
    4 / 8 / 12 beats, then the total nearest 17.5 s."""
    beat_len = 60.0 / bpm
    best = None
    for cp in sorted({want_cuts, want_cuts - 1, want_cuts + 1, want_cuts - 2, want_cuts + 2, 5, 6, 7, 8}):
        if cp < 3 or cp > 9:
            continue
        for b in (8, 12, 4, 6, 10, 16, 9, 7, 11, 5, 13, 14, 15):
            total = cp * b * beat_len
            if not dur_range[0] <= total <= dur_range[1]:
                continue
            score = (0 if b in (4, 8, 12) else 1,
                     abs(cp - want_cuts),
                     round(abs(total - 17.5), 3))
            if best is None or score < best[0]:
                best = (score, cp, b, round(b * beat_len, 6))
    if best is None:                      # no on-grid fit: fractional beats at requested count
        b = dur_range[0] / (want_cuts * beat_len)
        return want_cuts, round(b, 4), round(b * beat_len, 6)
    return best[1], best[2], best[3]


def music_start_for(music: dict, entry_beats: int, short_seconds: float = 20.0) -> float:
    """Grid-aligned music entry; backs off toward 0 if it would overrun the file."""
    bpm = float(music["bpm"])
    grid = float(music.get("grid_offset_seconds", 0.0))
    n = max(0, int(entry_beats))
    while n >= 0:
        start = grid + n * 60.0 / bpm
        if start + short_seconds <= float(music.get("duration", 1e9)) + 0.005:
            return round(start, 6)
        n -= 4
    return round(grid, 6)


def _pick_moments(cand: list[dict], t: np.ndarray, s: np.ndarray, center: float,
                  n: int, cd: float, dur: float, span: float,
                  blocked: list[tuple[float, float]]) -> list[float]:
    """Choose up to ``n`` cut starts (each ``cd`` long, non-overlapping, sorted
    by time) on the hottest instants within ``span`` seconds of ``center``.

    ``blocked`` is the list of (start, end) intervals already claimed by other
    shorts -- their footage is off limits so two montages never share a moment.
    Falls back to a contiguous slab only when the region has too few distinct
    sub-peaks to fill ``n`` cuts.
    """
    lo = max(0.0, center - span / 2.0)
    hi = min(dur, center + span / 2.0)

    hot = [dict(c) for c in cand if lo <= c["t"] <= hi]
    if len(hot) < n and len(s):
        m = (t >= lo) & (t <= hi)
        tm, sm = t[m], s[m]
        if len(sm) > 2:
            pk, _ = find_peaks(sm, distance=max(1, int(round(cd))))
            seen = {round(c["t"], 1) for c in hot}
            for i in pk:
                if round(float(tm[i]), 1) not in seen:
                    hot.append({"t": float(tm[i]), "score": float(sm[i])})
    hot.sort(key=lambda c: c["score"], reverse=True)

    starts: list[float] = []
    claimed = list(blocked)

    def _free(st: float) -> bool:
        seg0, seg1 = st, st + cd
        return not any(min(seg1, b) - max(seg0, a) > 0.05 for a, b in claimed)

    for c in hot:
        if len(starts) >= n:
            break
        st = min(max(lo, c["t"] - LEAD_FRAC * cd), dur - cd - 0.05)
        if not _free(st):
            continue
        starts.append(round(st, 3))
        claimed.append((st, st + cd))

    if len(starts) < n:                       # thin region: slab from its start
        base = min(max(lo, center - 0.4 * (n * cd)), dur - n * cd - 0.05)
        k = 0
        while len(starts) < n and k < n * 6:
            st = round(base + k * cd, 3)
            k += 1
            if _free(st):
                starts.append(st)
                claimed.append((st, st + cd))

    starts.sort()
    return starts[:n]


def autogroup(score: dict, cand: list[dict], batch_size: int = 5,
              cuts_per: int = C.DEFAULT_CUTS_PER_SHORT,
              music: dict | None = None, entry_beats: int = 0,
              spread: float | None = None) -> dict:
    """Each short is a ``cuts_per``-cut montage whose cuts sit on separate
    sub-peaks inside a hot region ``spread`` x the short length wide, so dead
    time between them is dropped rather than slabbed in. Regions never share
    footage."""
    file = score["file"]
    dur = score["duration"]
    spread = C.DEFAULT_SPREAD if spread is None else max(1.0, float(spread))
    t_arr = np.asarray(score.get("times", []), float)
    s_arr = np.asarray(score.get("smooth", []), float)
    track = resolve_music(music)
    cuts_per, beats, cd = fit_grid(float(track["bpm"]), cuts_per)
    window = cuts_per * cd                       # finished short length, on grid
    span = window * spread                       # how far we roam for sub-peaks
    mstart = music_start_for(track, entry_beats, window + 0.5)

    clusters: list[list[dict]] = []
    for c in cand:
        if clusters and c["t"] - clusters[-1][-1]["t"] <= C.CLUSTER_GAP_S:
            clusters[-1].append(c)
        else:
            clusters.append([c])

    ranked = []
    for cl in clusters:
        peak = max(cl, key=lambda x: x["score"])
        strength = sum(x["score"] for x in cl) + peak["score"]
        ranked.append({"peak": peak["t"], "strength": strength, "n": len(cl)})
    ranked.sort(key=lambda r: r["strength"], reverse=True)

    picked: list[dict] = []
    for r in ranked:
        if len(picked) >= batch_size:
            break
        if any(abs(r["peak"] - p["peak"]) < window * 1.1 for p in picked):
            continue
        picked.append(dict(r))
    picked.sort(key=lambda p: p["peak"])

    num = next_short_number()
    edits = []
    claimed: list[tuple[float, float]] = []
    for p in picked:
        if spread <= 1.0:                     # legacy: one contiguous ~20 s slab
            base = min(max(0.0, p["peak"] - 0.4 * window), dur - window - 0.05)
            starts = [round(base + k * cd, 3) for k in range(cuts_per)]
        else:
            starts = _pick_moments(cand, t_arr, s_arr, p["peak"], cuts_per, cd,
                                   dur, span, claimed)
        claimed.extend((st, st + cd) for st in starts)
        cuts = [
            _cut(file, st, dur, cd, beats,
                 f"Auto: regiao quente ~{p['peak']:.0f}s, corte {i+1}/{cuts_per} em {st:.1f}s.")
            for i, st in enumerate(starts)
        ]
        edits.append({
            "name": f"{num:02d}_AUTO",
            "title": "", "tag": "", "color": "#DAFF64",
            "music": {
                "file": track["file"], "sha256": track.get("sha256", ""),
                "bpm": track["bpm"],
                "grid_offset_seconds": track.get("grid_offset_seconds", 0.0),
                "evidence": track.get("evidence", "Grade confirmada pelo usuario no studio."),
            },
            "music_start": mstart,
            "cuts": cuts,
            "_peak": round(p["peak"], 2),
            "_entry_beats": entry_beats,
            "_score": round(p["strength"], 3),
        })
        num += 1

    return {"file": file, "sha": score["sha"], "duration": dur,
            "cut_seconds": round(cd, 4), "beats": beats, "cuts_per": cuts_per,
            "short_seconds": round(window, 3), "spread": round(spread, 3),
            "music": track, "candidates": cand, "edits": edits}


def _default_music() -> dict:
    d = json.loads((C.HARNESS / "defaults.json").read_text(encoding="utf-8-sig"))
    return d["music"]


if __name__ == "__main__":
    sc = json.loads((C.CACHE / sys.argv[1] / "score.json").read_text(encoding="utf8"))
    cand = candidates(sc)
    g = autogroup(sc, cand)
    print(f"{len(cand)} candidatos -> {len(g['edits'])} shorts rascunho")
    for e in g["edits"]:
        print(f"  {e['name']}  pico {e['_peak']}s  score {e['_score']}  "
              f"{len(e['cuts'])} cortes  {e['cuts'][0]['start']:.1f}..{e['cuts'][-1]['start']:.1f}")
