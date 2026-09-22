"""Turn labelled screenshots into a feature dataset for the scorer.

``frames/kill/*``  -> label 1  (momento de kill / bom momento)
``frames/nada/*``  -> label 0  (nada acontecendo)          [opcional]

Cada imagem vira **uma linha** de features: os sinais visuais + YOLO
(`person_*`, `enemy_*`) + a ROI de kill (`hit_center`) e `friendly_green`.
Uma foto não tem áudio nem tempo, então:

* ``audio_rms/hi/lo``      -> NaN
* ``motion``/``center_motion`` -> 0  (não há frame anterior)

Saída: ``studio/model/frames_dataset.csv`` (pra você olhar) + o mesmo em ``.npz``.
Opcional: negativos amostrados das gravações já em cache, mascarados para a mesma
disponibilidade de features (áudio NaN, movimento 0) para não vazar rótulo.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from pipeline import features  # noqa: E402

IMG_RE = re.compile(r"\.(jpe?g|png|webp|bmp)$", re.I)
AUDIO_COLS = [i for i, n in enumerate(features.FEATURE_NAMES) if n.startswith("audio_")]
MOTION_COLS = [features.FEATURE_NAMES.index(n) for n in ("motion", "center_motion")]
PERSON_COLS = [features.FEATURE_NAMES.index(n) for n in
               ("person_count", "person_conf", "person_area", "person_center", "person_area_sum")]
ENEMY_COLS = [features.FEATURE_NAMES.index(n) for n in
              ("enemy_count", "enemy_area", "enemy_center")]


def _label_dirs() -> list[tuple[Path, int]]:
    return [(C.FRAMES_DIR / "kill", 1), (C.FRAMES_DIR / "nada", 0)]


def iter_images() -> list[tuple[Path, int]]:
    out = []
    for d, label in _label_dirs():
        if d.is_dir():
            out += [(p, label) for p in sorted(d.iterdir()) if IMG_RE.search(p.name)]
    return out


def _load_yolo():
    try:
        from ultralytics import YOLO
        return YOLO(str(C.YOLO_WEIGHTS))
    except Exception as exc:  # noqa: BLE001
        print(f"[imgset] YOLO indisponivel ({exc}); person_/enemy_ ficam 0")
        return None


def image_row(path: Path, model=None) -> np.ndarray | None:
    """One feature row (len FEATURE_NAMES) for a still image, or None se ilegível."""
    import cv2

    bgr = cv2.imread(str(path))
    if bgr is None:
        return None
    h0, w0 = bgr.shape[:2]
    w = C.ANALYSIS_WIDTH
    h = int(round(w * h0 / w0 / 2) * 2)
    bgr = cv2.resize(bgr, (w, h))
    row, _ = features.visual_row(bgr, None, features.geom(w, h))
    if model is not None:
        st = features._yolo_person_stats([bgr], model)[0]
        row[PERSON_COLS] = st[:5]
        row[ENEMY_COLS] = st[5:8]
    row[AUDIO_COLS] = np.nan            # foto não tem áudio
    return row


def _negatives_from_cache(n: int, rng) -> list[np.ndarray]:
    """Amostra `n` frames dos caches de gravação, mascarando áudio/movimento
    para casar com o que uma foto tem."""
    npzs = sorted(C.CACHE.glob("*/features.npz"))
    if not npzs or n <= 0:
        return []
    per = max(1, n // len(npzs))
    rows = []
    for p in npzs:
        try:
            d = np.load(p, allow_pickle=True)
            X, _ = features._align_to_current(d["X"], list(d["names"]))
        except Exception:  # noqa: BLE001
            continue
        if len(X) == 0:
            continue
        idx = rng.choice(len(X), size=min(per, len(X)), replace=False)
        for r in X[idx]:
            r = r.astype(np.float32).copy()
            r[AUDIO_COLS] = np.nan
            r[MOTION_COLS] = 0.0
            rows.append(r)
    return rows[:n]


def build(neg_from_recordings: int = 0) -> dict:
    imgs = iter_images()
    if not imgs and neg_from_recordings <= 0:
        raise RuntimeError(
            f"Sem imagens em {C.FRAMES_DIR/'kill'} nem {C.FRAMES_DIR/'nada'}. "
            "Coloque prints .png/.jpg dos momentos.")
    model = _load_yolo() if imgs else None
    X, y, paths = [], [], []
    for i, (p, label) in enumerate(imgs):
        r = image_row(p, model)
        if r is None:
            print(f"  ilegivel: {p.name}")
            continue
        X.append(r)
        y.append(label)
        paths.append(p.relative_to(C.ROOT).as_posix())
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(imgs)}")
    if neg_from_recordings > 0:
        extra = _negatives_from_cache(neg_from_recordings, np.random.default_rng(0))
        X += extra
        y += [0] * len(extra)
        paths += [f"cache:sample:{k}" for k in range(len(extra))]
        print(f"  + {len(extra)} negativos amostrados das gravacoes em cache")
    if not X:
        raise RuntimeError("Nenhuma linha gerada.")
    return {"X": np.vstack(X).astype(np.float32), "y": np.array(y, int),
            "names": list(features.FEATURE_NAMES), "paths": paths}


def write_csv(d: dict, dest: Path | None = None) -> Path:
    dest = dest or (C.MODEL_DIR / "frames_dataset.csv")
    with open(dest, "w", newline="", encoding="utf8") as f:
        wr = csv.writer(f)
        wr.writerow(["path", "label", *d["names"]])
        for path, label, row in zip(d["paths"], d["y"], d["X"]):
            wr.writerow([path, int(label),
                         *(f"{v:.5f}" if np.isfinite(v) else "" for v in row)])
    np.savez_compressed(dest.with_suffix(".npz"), X=d["X"], y=d["y"],
                        names=np.array(d["names"]), paths=np.array(d["paths"]))
    return dest


def train_frames(d: dict | None = None) -> dict:
    """HGBC nos frames rotulados. Descarta as colunas de áudio (sempre NaN aqui)."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.metrics import average_precision_score, roc_auc_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict

    d = d or build()
    keep = [i for i, n in enumerate(d["names"]) if not n.startswith("audio_")]
    X, y = d["X"][:, keep], d["y"]
    names = [d["names"][i] for i in keep]
    if len(set(y)) < 2:
        raise RuntimeError("Precisa de imagens em frames/kill/ E frames/nada/ "
                           "(ou use --neg-recordings N).")

    def _m():
        return HistGradientBoostingClassifier(
            max_iter=300, learning_rate=0.05, max_depth=5,
            l2_regularization=1.0, random_state=0)

    rep = {}
    counts = np.bincount(y)
    if counts.min() >= 3:
        k = int(min(5, counts.min()))
        oof = cross_val_predict(_m(), X, y, method="predict_proba",
                                cv=StratifiedKFold(k, shuffle=True, random_state=0))[:, 1]
        rep = {"scheme": f"StratifiedKFold({k})",
               "roc_auc": round(float(roc_auc_score(y, oof)), 4),
               "avg_precision": round(float(average_precision_score(y, oof)), 4)}
    model = _m().fit(X, y)
    meta = {
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "kind": "frames", "n_rows": int(len(y)),
        "n_pos": int(y.sum()), "n_neg": int((y == 0).sum()),
        "n_features": len(names), "feature_names": names, "validation": rep,
    }
    import joblib
    joblib.dump({"model": model, "names": names, "meta": meta},
                C.MODEL_DIR / "scorer_frames.joblib")
    (C.MODEL_DIR / "scorer_frames_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf8")
    return meta


if __name__ == "__main__":
    neg = 0
    for a in sys.argv:
        if a.startswith("--neg-recordings="):
            neg = int(a.split("=", 1)[1])
    d = build(neg_from_recordings=neg)
    dest = write_csv(d)
    print(f"\n{len(d['y'])} linhas ({int(d['y'].sum())} kill / {int((d['y']==0).sum())} nada) "
          f"-> {dest.relative_to(C.ROOT)}  (+ .npz)")
    if "--train" in sys.argv:
        m = train_frames(d)
        print(json.dumps(m["validation"], ensure_ascii=False, indent=2))
