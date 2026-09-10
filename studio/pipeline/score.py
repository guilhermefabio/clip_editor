"""Score every sampled frame of a source and cache the interest curve."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import joblib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from pipeline import derive, features  # noqa: E402


def _smooth(a: np.ndarray, half: int) -> np.ndarray:
    if half <= 0 or len(a) == 0:
        return a
    k = np.ones(2 * half + 1) / (2 * half + 1)
    return np.convolve(a, k, mode="same")


def load_scorer():
    if not C.SCORER_PATH.exists():
        raise RuntimeError("Modelo ausente. Rode: python studio/pipeline/train.py")
    return joblib.load(C.SCORER_PATH)


def score_source(path: Path, progress=None, force: bool = False) -> dict:
    path = Path(path)
    bundle = load_scorer()
    f = features.extract(path, progress=lambda p, m: progress and progress(0.8 * p, m))
    digest = f["sha"]
    cdir = C.CACHE / digest
    cdir.mkdir(parents=True, exist_ok=True)
    out_json = cdir / "score.json"

    if out_json.exists() and not force:
        cached = json.loads(out_json.read_text(encoding="utf8"))
        if cached.get("model_at") == bundle["meta"]["trained_at"]:
            return cached

    if progress:
        progress(0.85, "aplicando modelo")
    t = f["times"]
    Xa, names = derive.augment(t, f["X"], f["names"], C.FPS_ANALYSIS)
    if names != bundle["names"]:
        # Align columns defensively if feature layout drifted.
        idx = [names.index(n) for n in bundle["names"] if n in names]
        Xa = Xa[:, idx]
    raw = bundle["model"].predict_proba(Xa)[:, 1] if len(t) else np.array([])
    smooth = _smooth(raw, int(round(0.6 * C.FPS_ANALYSIS)))

    result = {
        "file": path.name, "sha": digest,
        "duration": f["meta"]["duration"], "fps_analysis": C.FPS_ANALYSIS,
        "model_at": bundle["meta"]["trained_at"],
        "threshold": bundle["meta"]["suggested_threshold"],
        "times": [round(float(x), 3) for x in t],
        "raw": [round(float(x), 4) for x in raw],
        "smooth": [round(float(x), 4) for x in smooth],
    }
    out_json.write_text(json.dumps(result), encoding="utf8")
    np.savez_compressed(cdir / "score.npz", times=t, raw=raw, smooth=smooth)
    if progress:
        progress(1.0, "score pronto")
    return result


if __name__ == "__main__":
    r = score_source(Path(sys.argv[1]), progress=lambda p, m: print(f"  {p*100:5.1f}%  {m}", end="\r"))
    s = np.array(r["smooth"])
    print(f"\n{r['file']}: {len(s)} frames  max={s.max():.3f}  thr={r['threshold']:.3f}  "
          f"acima={int((s > r['threshold']).sum())}")
