"""imgset: prints rotulados -> linhas de features (uma foto = uma linha)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import config as C  # noqa: E402
from pipeline import features, imgset  # noqa: E402

cv2 = pytest.importorskip("cv2")
N = len(features.FEATURE_NAMES)
AUDIO = [i for i, n in enumerate(features.FEATURE_NAMES) if n.startswith("audio_")]


def _png(path, w=320, h=180, val=90):
    img = np.full((h, w, 3), val, np.uint8)
    cv2.rectangle(img, (w // 3, h // 3), (2 * w // 3, 2 * h // 3), (200, 200, 200), 2)
    cv2.imwrite(str(path), img)


@pytest.fixture
def frames_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "FRAMES_DIR", tmp_path / "frames")
    (tmp_path / "frames" / "kill").mkdir(parents=True)
    (tmp_path / "frames" / "nada").mkdir(parents=True)
    return tmp_path / "frames"


def test_image_row_shape_and_masking(frames_dir):
    p = frames_dir / "kill" / "a.png"
    _png(p)
    row = imgset.image_row(p, model=None)
    assert row.shape == (N,)
    assert np.isnan(row[AUDIO]).all()                       # foto não tem áudio
    assert row[features.FEATURE_NAMES.index("motion")] == 0  # sem frame anterior
    assert np.isfinite(row[features.FEATURE_NAMES.index("edge_density")])


def test_image_row_none_on_unreadable(frames_dir):
    bad = frames_dir / "kill" / "x.png"
    bad.write_bytes(b"not a png")
    assert imgset.image_row(bad, model=None) is None


def test_build_labels_by_subfolder(frames_dir, monkeypatch):
    for i in range(3):
        _png(frames_dir / "kill" / f"k{i}.png", val=60)
        _png(frames_dir / "nada" / f"n{i}.png", val=140)
    monkeypatch.setattr(imgset, "_load_yolo", lambda: None)
    d = imgset.build()
    assert d["X"].shape == (6, N)
    assert sorted(d["y"]) == [0, 0, 0, 1, 1, 1]
    assert all(pth.endswith(".png") for pth in d["paths"])
    # rótulo casa com a subpasta
    for pth, lab in zip(d["paths"], d["y"]):
        assert ("/kill/" in pth) == (lab == 1)


def test_build_empty_raises(frames_dir):
    with pytest.raises(RuntimeError, match="Sem imagens"):
        imgset.build()


def test_write_csv_roundtrip(frames_dir, monkeypatch, tmp_path):
    for i in range(2):
        _png(frames_dir / "kill" / f"k{i}.png")
        _png(frames_dir / "nada" / f"n{i}.png")
    monkeypatch.setattr(imgset, "_load_yolo", lambda: None)
    d = imgset.build()
    dest = imgset.write_csv(d, tmp_path / "ds.csv")
    lines = dest.read_text(encoding="utf8").splitlines()
    assert lines[0].startswith("path,label,motion,")
    assert len(lines) == 1 + 4
    assert dest.with_suffix(".npz").exists()
