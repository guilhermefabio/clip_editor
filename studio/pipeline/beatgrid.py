"""Music track registry + beat-grid estimation for the studio.

Known tracks (BPM + grid offset already confirmed in ``defaults.json`` or an
approved plan) are returned as-is. For an unknown track we estimate the grid
from the percussion onset envelope and hand the top candidates to the user to
confirm -- the harness will not accept a track without ``evidence``.
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

AUDIO_EXT = (".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg")


def _sha(p: Path) -> str:
    with open(p, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def _known_grids() -> dict:
    """sha256 -> {bpm, grid_offset_seconds, evidence} from every plan on disk."""
    out: dict[str, dict] = {}
    files = [C.HARNESS / "defaults.json", *C.HARNESS.glob("plano_*.json"),
             *C.ROOT.glob("*/projeto/edicao.json")]
    for f in files:
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError):
            continue
        blocks = []
        if isinstance(d, dict):
            if d.get("music"):
                blocks.append(d["music"])
            blocks += [e["music"] for e in d.get("edits", [])
                       if isinstance(e, dict) and e.get("music")]
        for m in blocks:
            sha = str(m.get("sha256", "")).lower()
            if sha and "bpm" in m and sha not in out:
                out[sha] = {
                    "bpm": float(m["bpm"]),
                    "grid_offset_seconds": float(m.get("grid_offset_seconds", 0)),
                    "evidence": m.get("evidence", "Grade herdada de plano aprovado."),
                }
    return out


def _duration(p: Path) -> float:
    try:
        out = subprocess.check_output(
            [str(C.FFPROBE), "-v", "error", "-show_entries", "format=duration",
             "-of", "json", str(p)])
        return float(json.loads(out)["format"]["duration"])
    except Exception:  # noqa: BLE001
        return 0.0


def registry() -> list[dict]:
    known = _known_grids()
    items = []
    candidates = sorted(C.ROOT.glob("*")) + sorted(C.AUDIO_DIR.glob("*"))
    for p in candidates:
        if p.suffix.lower() not in AUDIO_EXT or not p.is_file():
            continue
        sha = _sha(p)
        # relative to ROOT (e.g. "audio/beat_phonk.wav") -- this is what gets
        # written into a plan's music.file and resolved as root/plan['music']['file']
        rec = {"file": p.relative_to(C.ROOT).as_posix(), "sha256": sha, "duration": round(_duration(p), 2)}
        if sha in known:
            rec.update(known[sha])
            rec["known"] = True
        else:
            rec["known"] = False
        items.append(rec)
    return items


def estimate(path: Path, bpm_lo: float = 100.0, bpm_hi: float = 180.0) -> dict:
    """Return {candidates: [[strength, bpm, phase], ...], evidence}."""
    raw = subprocess.check_output(
        [str(C.FFMPEG), "-v", "error", "-i", str(path),
         "-ac", "1", "-ar", "12000", "-f", "f32le", "-"])
    a = np.frombuffer(raw, np.float32)
    if a.size < 12000:
        return {"candidates": [], "evidence": "Audio curto demais para estimar."}

    from scipy.signal import butter, sosfilt, find_peaks

    hi = sosfilt(butter(3, 1800, fs=12000, btype="high", output="sos"), a)
    win = 60  # 5 ms @ 12 kHz -> 200 Hz envelope
    env = np.sqrt(np.mean(hi[:len(hi) // win * win].reshape(-1, win) ** 2, axis=1))
    env = env / (env.max() or 1.0)
    env_sr = 12000 / win

    scores = []
    for bpm in np.arange(bpm_lo, bpm_hi + 0.01, 0.1):
        period = 60.0 / bpm
        phases = np.arange(0, period, 0.005)
        best_v, best_p = 0.0, 0.0
        grid_t = np.arange(0, len(a) / 12000, period)
        for off in phases:
            idx = np.clip(((grid_t + off) * env_sr).astype(int), 0, len(env) - 1)
            v = float(env[idx].mean())
            if v > best_v:
                best_v, best_p = v, float(off)
        scores.append((round(best_v, 4), round(float(bpm), 2), round(best_p, 3)))
    scores.sort(reverse=True)
    top = scores[:10]
    peaks, _ = find_peaks(env, distance=int(env_sr * 0.18), prominence=0.12)
    ev = (f"Envelope de percussao > 1800 Hz, RMS 5 ms. Melhor grade "
          f"{top[0][1]} BPM, fase {top[0][2]} s (score {top[0][0]}). "
          f"{len(peaks)} ataques detectados nos primeiros {len(a)/12000:.0f} s.")
    return {"candidates": top, "evidence": ev}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(estimate(Path(sys.argv[1])), indent=2, ensure_ascii=False))
    else:
        for r in registry():
            print(f"{r['file']:34s} {r['duration']:6.1f}s  "
                  f"{'BPM ' + str(r.get('bpm')) + ' / ' + str(r.get('grid_offset_seconds')) if r['known'] else 'grade desconhecida'}")
