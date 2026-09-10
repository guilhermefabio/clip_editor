"""Fit the lightweight "frame of interest" scorer.

Positives/negatives come from :mod:`pipeline.dataset` (the approved cuts).
Validation is grouped by source when more than one gameplay is on disk, and
falls back to a temporal hold-out (last 25 % of the timeline) when everything
comes from a single recording.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import GroupKFold
import joblib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from pipeline import dataset  # noqa: E402


def _model() -> HistGradientBoostingClassifier:
    return HistGradientBoostingClassifier(
        max_iter=400, learning_rate=0.05, max_depth=6,
        l2_regularization=1.0, early_stopping=True, validation_fraction=0.15,
        random_state=0)


def _prf(y, p, thr):
    pred = p >= thr
    tp = int((pred & (y == 1)).sum())
    fp = int((pred & (y == 0)).sum())
    fn = int((~pred & (y == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3)}


def _evaluate(X, y, g, tt):
    """Return (report dict, held-out scores, held-out labels).

    The held-out scores are genuine out-of-fold / out-of-time predictions and
    are what the interest threshold is calibrated on.
    """
    n_groups = len(set(g))
    if n_groups >= 2:
        k = min(5, n_groups)
        oof = np.zeros(len(y))
        for tr, te in GroupKFold(k).split(X, y, g):
            m = _model().fit(X[tr], y[tr])
            oof[te] = m.predict_proba(X[te])[:, 1]
        report = {"scheme": f"GroupKFold({k}) por fonte",
                  "roc_auc": round(float(roc_auc_score(y, oof)), 4),
                  "avg_precision": round(float(average_precision_score(y, oof)), 4),
                  "n_holdout": int(len(y))}
        return report, oof, y
    cut = np.quantile(tt, 0.75)
    tr, te = tt <= cut, tt > cut
    if te.sum() < 20 or len(set(y[te])) < 2:
        return {"scheme": "sem holdout confiavel (fonte unica, poucos dados)"}, None, None
    m = _model().fit(X[tr], y[tr])
    p = m.predict_proba(X[te])[:, 1]
    report = {"scheme": "hold-out temporal (ultimos 25% da gravacao)",
              "roc_auc": round(float(roc_auc_score(y[te], p)), 4),
              "avg_precision": round(float(average_precision_score(y[te], p)), 4),
              "n_holdout": int(te.sum())}
    return report, p, y[te]


def _importances(model, X, y, names, n_repeats=6):
    try:
        n = min(4000, len(y))
        idx = np.random.default_rng(0).choice(len(y), n, replace=False)
        r = permutation_importance(model, X[idx], y[idx], n_repeats=n_repeats,
                                   random_state=0, scoring="roc_auc", n_jobs=1)
        order = np.argsort(r.importances_mean)[::-1][:12]
        return [{"feature": names[i], "importance": round(float(r.importances_mean[i]), 4)}
                for i in order if r.importances_mean[i] > 0]
    except Exception as exc:  # noqa: BLE001
        print(f"[train] importancia indisponivel: {exc}")
        return []


def train(progress=None, raw_only: bool = False) -> dict:
    if progress:
        progress(0.05, "coletando gravacoes brutas" if raw_only
                 else "coletando gravacoes brutas + clipes de kill")
    data = dataset.build(
        progress=lambda p, m: progress and progress(0.05 + 0.55 * p, m),
        use_kill_clips=not raw_only)
    X, y, g, names, tt = data["X"], data["y"], data["groups"], data["names"], data["times"]

    if progress:
        progress(0.62, "validando")
    report, held_p, held_y = _evaluate(X, y, g, tt)

    if progress:
        progress(0.8, "treinando modelo final")
    model = _model().fit(X, y)

    # Calibrate the interest threshold on genuine held-out predictions.
    if held_p is not None:
        pos = np.sort(held_p[held_y == 1])
        thr = float(np.clip(np.quantile(pos, 0.35), 0.3, 0.8)) if len(pos) else 0.5
        report.update(_prf(held_y, held_p, thr))
    else:
        pos = np.sort(model.predict_proba(X)[:, 1][y == 1])
        thr = float(np.clip(np.quantile(pos, 0.5), 0.3, 0.85)) if len(pos) else 0.5

    if progress:
        progress(0.9, "medindo importancia das features")
    top_features = _importances(model, X, y, names)

    meta = {
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "raw_only": bool(raw_only),
        "source": "gravacoes brutas" if raw_only else "gravacoes brutas + clipes_kill/",
        "n_kill_clips": sum(1 for s in data["sources"] if s.get("kind") == "kill_clip"),
        "audio_used": any(n.startswith("audio_") for n in names),
        "n_rows": int(len(y)),
        "n_pos": int(y.sum()),
        "n_neg": int((y == 0).sum()),
        "n_features": len(names),
        "n_sources": len(data["sources"]),
        "sources": data["sources"],
        "feature_names": names,
        "validation": report,
        "suggested_threshold": round(thr, 3),
        "fps_analysis": C.FPS_ANALYSIS,
        "top_features": top_features,
    }
    joblib.dump({"model": model, "names": names, "meta": meta}, C.SCORER_PATH)
    (C.MODEL_DIR / "scorer_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf8")
    if progress:
        progress(1.0, "modelo salvo")
    return meta


if __name__ == "__main__":
    raw_only = "--raw-only" in sys.argv
    m = train(progress=lambda p, x: print(f"  {p*100:5.1f}%  {x}"), raw_only=raw_only)
    print(json.dumps(m["validation"], ensure_ascii=False, indent=2))
    print(f"threshold sugerido: {m['suggested_threshold']:.3f}   "
          f"({m['n_pos']} pos / {m['n_neg']} neg / {m['n_sources']} fonte(s))")
    print("top features:", ", ".join(f"{t['feature']}={t['importance']}" for t in m["top_features"][:6]))
