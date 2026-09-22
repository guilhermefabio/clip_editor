"""Fit the lightweight "frame of interest" scorer.

Positives/negatives come from :mod:`pipeline.dataset` (the approved cuts).
Validation is grouped by source when more than one gameplay is on disk, and
requires at least two known recording groups. Unknown origins are excluded
from validation but retained for the final training fit.
"""
from __future__ import annotations

import json
import re
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


def _cv_groups(g):
    """Unify recording IDs across video/stills; unresolved origins never enter CV.

    Optional local provenance maps legacy group IDs (e.g. kill:clip or
    unknown:frame:name) to the original recording's full SHA-256.
    """
    manifest = C.MODEL_DIR / "provenance.json"
    mapping = json.loads(manifest.read_text(encoding="utf8")) if manifest.exists() else {}
    result = []
    for value in g:
        value = str(value)
        if value in mapping:
            sha = mapping[value]
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", sha):
                raise ValueError("provenance.json values must be full recording SHA-256 hashes")
            value = sha.lower()[:12]
        elif value.startswith("frame:"):
            value = value[6:]
        elif value.startswith(("unknown:", "kill:")):
            value = ""
        result.append(value.lower())
    return np.asarray(result)


def _evaluate(X, y, g, tt):
    """Recording-disjoint OOF evaluation. Unknown provenance is excluded.

    A single recording cannot estimate cross-recording generalization; no
    frame-level or temporal fallback is presented as independent validation.
    """
    g = _cv_groups(g)
    known = g != ""
    X, y, g = X[known], y[known], g[known]
    n_groups = len(set(g))
    report = {"scheme": "recording-disjoint GroupKFold", "n_cv_groups": n_groups,
              "n_excluded_unknown_origin": int((~known).sum()), "n_folds": 0,
              "folds": [], "threshold_evaluation": "fixed 0.5; not tuned on OOF"}
    for key in ("roc_auc", "avg_precision"):
        report.update({key + "_mean": None, key + "_std": None,
                       key + "_valid_folds": 0})
    report["n_holdout"] = 0
    if n_groups < 2:
        report["limitation"] = "At least two known recording groups are required"
        return report, None, None
    k = min(5, n_groups)
    report["n_folds"] = k
    oof = np.full(len(y), np.nan)
    for fold, (tr, te) in enumerate(GroupKFold(k).split(X, y, g), 1):
        detail = {"fold": fold, "n_train": len(tr), "n_test": len(te),
                  "train_pos": int(y[tr].sum()), "train_neg": int((y[tr] == 0).sum()),
                  "test_pos": int(y[te].sum()), "test_neg": int((y[te] == 0).sum())}
        if len(set(y[tr])) < 2:
            detail.update(status="skipped: single-class training fold", roc_auc=None, avg_precision=None)
        else:
            p = _model().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
            oof[te] = p
            both = len(set(y[te])) == 2
            detail.update(status="evaluated", **_prf(y[te], p, 0.5),
                          roc_auc=float(roc_auc_score(y[te], p)) if both else None,
                          avg_precision=float(average_precision_score(y[te], p)) if both else None)
        report["folds"].append(detail)
    for key in ("roc_auc", "avg_precision"):
        values = [f[key] for f in report["folds"] if f[key] is not None]
        report[key + "_mean"] = float(np.mean(values)) if values else None
        report[key + "_std"] = float(np.std(values)) if values else None
        report[key + "_valid_folds"] = len(values)
    valid = np.isfinite(oof)
    report["n_holdout"] = int(valid.sum())
    report["n_unscored_known_origin"] = int((~valid).sum())
    if not valid.all():
        report["limitation"] = "Some folds lack both training classes; pooled metrics cover scored rows only"
    if not valid.any() or len(set(y[valid])) < 2:
        return report, None, None
    p, labels = oof[valid], y[valid]
    report.update(roc_auc=float(roc_auc_score(labels, p)),
                  avg_precision=float(average_precision_score(labels, p)),
                  **_prf(labels, p, 0.5), evaluation_threshold=0.5)
    return report, p, labels


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
                 else "coletando gravacoes brutas + clipes de kill + frames revisados")
    data = dataset.build(
        progress=lambda p, m: progress and progress(0.05 + 0.55 * p, m),
        use_kill_clips=not raw_only, use_review_frames=not raw_only)
    X, y, g, names, tt = data["X"], data["y"], data["groups"], data["names"], data["times"]

    if progress:
        progress(0.62, "validando")
    report, held_p, held_y = _evaluate(X, y, g, tt)

    if progress:
        progress(0.8, "treinando modelo final")
    model = _model().fit(X, y)

    # Operational suggestion only: tuning and reporting on the same OOF data
    # would be optimistic. Primary PR/F1 above use the predeclared 0.5 threshold.
    thr = 0.5
    if held_p is not None:
        pos = held_p[held_y == 1]
        thr = float(np.clip(np.quantile(pos, 0.35), 0.3, 0.8)) if len(pos) else 0.5
        report["tuned_threshold_diagnostic"] = {
            "threshold": thr, **_prf(held_y, held_p, thr),
            "limitation": "Selected and measured on the same OOF predictions; not independent"}

    if progress:
        progress(0.9, "medindo importancia das features")
    top_features = _importances(model, X, y, names)

    meta = {
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "raw_only": bool(raw_only),
        "source": ("gravacoes brutas" if raw_only
                   else "gravacoes brutas + clipes_kill/ + frames revisados"),
        "n_kill_clips": sum(1 for s in data["sources"] if s.get("kind") == "kill_clip"),
        "n_review_pos": sum(s.get("pos", 0) for s in data["sources"] if s.get("kind") == "frame_review"),
        "n_review_neg": sum(s.get("neg", 0) for s in data["sources"] if s.get("kind") == "frame_review"),
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
