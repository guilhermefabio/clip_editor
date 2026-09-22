"""Regras de colheita do dataset de treino do scorer (esquema de 2026-09-09).

Positivos = clipes crus de kill (``clipes_kill/``) + frames dentro dos cortes
aprovados das gravações. Negativos = frames fora dos cortes, nas gravações.
Áudio sempre dentro. Sem Shorts renderizados.

Os testes trocam ``config.KILL_CLIPS_DIR`` por um tmp e dublam
``features.extract`` / ``load_cached`` / ``source_meta`` e ``_cut_groups`` para
não decodificar vídeo.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import config as C  # noqa: E402
from pipeline import dataset, features  # noqa: E402

N_BASE = len(features.FEATURE_NAMES)  # 19


def _synth_feats(n=180, sha="deadbeef", seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / C.FPS_ANALYSIS
    X = np.abs(rng.normal(0.1, 0.05, size=(n, N_BASE))).astype(np.float32)
    return {"times": t.astype(np.float32), "X": X,
            "names": list(features.FEATURE_NAMES), "sha": sha,
            "meta": {"duration": float(n / C.FPS_ANALYSIS)}}


REC_GROUPS = {
    "deadbeef": {"file": "grav.mkv", "sha": "deadbeef",
                 "intervals": [(5.0, 15.0), (30.0, 40.0)],
                 "has_cache": True, "has_file": False},
}


@pytest.fixture(autouse=True)
def frames_dir(tmp_path, monkeypatch):
    """Isolate frames/ + model/ so tests never touch the real reviewed dataset
    or write into the real cache file."""
    monkeypatch.setattr(C, "FRAMES_DIR", tmp_path / "frames")
    monkeypatch.setattr(C, "MODEL_DIR", tmp_path / "model")
    return tmp_path / "frames"


@pytest.fixture
def kill_dir(tmp_path, monkeypatch):
    d = tmp_path / "clipes_kill"
    d.mkdir()
    monkeypatch.setattr(C, "KILL_CLIPS_DIR", d)
    return d


@pytest.fixture
def stubs(monkeypatch):
    calls = []

    def fake_extract(path, *a, **k):
        calls.append(Path(path).name)
        return _synth_feats(sha=f"clip{len(calls)}", seed=len(calls))

    monkeypatch.setattr(dataset.features, "extract", fake_extract)
    monkeypatch.setattr(dataset.features, "load_cached", lambda sha: _synth_feats(sha=sha))
    monkeypatch.setattr(dataset.features, "source_meta", lambda p: {"duration": 12.0})
    return calls


# --------------------------------------------------------------- iter_kill_clips
def test_iter_takes_any_mp4_in_the_folder(kill_dir, stubs):
    (kill_dir / "kill_um.mp4").write_bytes(b"x")
    (kill_dir / "outro corte.mp4").write_bytes(b"x")
    (kill_dir / "LEIA.txt").write_text("nao e video")
    got = dataset.iter_kill_clips()
    assert sorted(p.name for p, _ in got) == ["kill_um.mp4", "outro corte.mp4"]
    assert all(gid.startswith("kill:") for _, gid in got)


def test_iter_skips_clips_outside_the_kill_window(kill_dir, monkeypatch):
    (kill_dir / "curto.mp4").write_bytes(b"x")
    (kill_dir / "ok.mp4").write_bytes(b"x")
    durs = {"curto.mp4": 1.5, "ok.mp4": 12.0}
    monkeypatch.setattr(dataset.features, "source_meta",
                        lambda p: {"duration": durs[Path(p).name]})
    got = [p.name for p, _ in dataset.iter_kill_clips()]
    assert got == ["ok.mp4"]


def test_iter_missing_dir_is_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "KILL_CLIPS_DIR", tmp_path / "nao_existe")
    assert dataset.iter_kill_clips() == []


# --------------------------------------------------------------- build()
def test_build_mixes_recordings_and_kill_clips(kill_dir, stubs, monkeypatch):
    (kill_dir / "k1.mp4").write_bytes(b"x")
    (kill_dir / "k2.mp4").write_bytes(b"x")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: dict(REC_GROUPS))
    data = dataset.build()
    kinds = sorted({s["kind"] for s in data["sources"]})
    assert kinds == ["gravacao", "kill_clip"]
    assert sum(s["kind"] == "kill_clip" for s in data["sources"]) == 2
    assert set(np.unique(data["y"])) == {0.0, 1.0}


def test_build_keeps_audio_bands(kill_dir, stubs, monkeypatch):
    (kill_dir / "k1.mp4").write_bytes(b"x")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: dict(REC_GROUPS))
    data = dataset.build()
    assert any(n.startswith("audio_") for n in data["names"])


def test_build_kill_clip_frames_are_all_positive(kill_dir, stubs, monkeypatch):
    (kill_dir / "k1.mp4").write_bytes(b"x")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: dict(REC_GROUPS))
    data = dataset.build()
    clip_rows = [s for s in data["sources"] if s["kind"] == "kill_clip"][0]
    assert clip_rows["neg"] == 0 and clip_rows["pos"] > 0


def test_build_raw_only_ignores_kill_clips(kill_dir, stubs, monkeypatch):
    (kill_dir / "k1.mp4").write_bytes(b"x")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: dict(REC_GROUPS))
    data = dataset.build(use_kill_clips=False)
    assert {s["kind"] for s in data["sources"]} == {"gravacao"}


def test_build_without_any_source_raises(kill_dir, stubs, monkeypatch):
    monkeypatch.setattr(dataset, "_cut_groups", lambda: {})
    with pytest.raises(RuntimeError, match="Sem fontes de treino"):
        dataset.build()


def test_build_kill_clips_but_no_recordings_raises(kill_dir, stubs, monkeypatch):
    (kill_dir / "k1.mp4").write_bytes(b"x")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: {})
    with pytest.raises(RuntimeError, match="NEGATIVO"):
        dataset.build()


def test_build_groups_keep_clips_and_recording_apart(kill_dir, stubs, monkeypatch):
    (kill_dir / "k1.mp4").write_bytes(b"x")
    (kill_dir / "k2.mp4").write_bytes(b"x")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: dict(REC_GROUPS))
    data = dataset.build()
    assert len(set(data["groups"])) == 3  # 1 gravação + 2 clipes


# --------------------------------------------------------------- iter_review_frames
def _touch(p):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"x")


def test_iter_review_frames_groups_by_embedded_sha(frames_dir):
    _touch(frames_dir / "kill" / "gt_aaaaaaaaaaaa_f0000010.jpg")
    _touch(frames_dir / "kill" / "gt_aaaaaaaaaaaa_f0000020.jpg")
    _touch(frames_dir / "nada" / "gt_bbbbbbbbbbbb_f0000000.jpg")
    _touch(frames_dir / "nada" / "estranho.jpg")
    got = {p.name: (label, gid) for p, label, gid in dataset.iter_review_frames()}
    assert got["gt_aaaaaaaaaaaa_f0000010.jpg"] == (1, "frame:aaaaaaaaaaaa")
    assert got["gt_aaaaaaaaaaaa_f0000020.jpg"] == (1, "frame:aaaaaaaaaaaa")
    assert got["gt_bbbbbbbbbbbb_f0000000.jpg"] == (0, "frame:bbbbbbbbbbbb")
    assert got["estranho.jpg"] == (0, "frame:estranho")


def test_iter_review_frames_missing_dirs_is_empty(frames_dir):
    assert dataset.iter_review_frames() == []


# --------------------------------------------------------------- build() + reviewed frames
def _fake_row(seed):
    rng = np.random.default_rng(seed)
    return np.abs(rng.normal(0.1, 0.05, size=N_BASE)).astype(np.float32)


@pytest.fixture
def review_stub(monkeypatch):
    monkeypatch.setattr(dataset.imgset, "_load_yolo", lambda: None)
    monkeypatch.setattr(dataset.imgset, "image_row",
                        lambda p, model: _fake_row(abs(hash(p.name)) % 1000))


def test_build_folds_in_review_frames_alone(frames_dir, review_stub, monkeypatch):
    _touch(frames_dir / "kill" / "gt_aaaaaaaaaaaa_f0000010.jpg")
    _touch(frames_dir / "kill" / "gt_aaaaaaaaaaaa_f0000020.jpg")
    _touch(frames_dir / "nada" / "gt_bbbbbbbbbbbb_f0000000.jpg")
    _touch(frames_dir / "nada" / "gt_bbbbbbbbbbbb_f0000005.jpg")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: {})
    data = dataset.build(use_kill_clips=False)
    fr = [s for s in data["sources"] if s["kind"] == "frame_review"][0]
    assert fr["pos"] == 2 and fr["neg"] == 2
    assert set(np.unique(data["y"])) == {0.0, 1.0}
    assert set(data["groups"]) == {"frame:aaaaaaaaaaaa", "frame:bbbbbbbbbbbb"}


def test_build_review_frames_cache_avoids_recompute(frames_dir, monkeypatch):
    _touch(frames_dir / "kill" / "gt_aaaaaaaaaaaa_f0000010.jpg")
    _touch(frames_dir / "nada" / "gt_bbbbbbbbbbbb_f0000000.jpg")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: {})
    calls = []

    def counting_row(p, model):
        calls.append(p.name)
        return _fake_row(len(calls))

    monkeypatch.setattr(dataset.imgset, "_load_yolo", lambda: None)
    monkeypatch.setattr(dataset.imgset, "image_row", counting_row)
    dataset.build(use_kill_clips=False)
    assert len(calls) == 2
    dataset.build(use_kill_clips=False)
    assert len(calls) == 2  # segunda chamada reaproveita o cache em disco


def test_build_raw_only_ignores_review_frames(frames_dir, kill_dir, stubs, review_stub, monkeypatch):
    _touch(frames_dir / "kill" / "gt_aaaaaaaaaaaa_f0000010.jpg")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: dict(REC_GROUPS))
    data = dataset.build(use_kill_clips=False, use_review_frames=False)
    assert "frame_review" not in {s["kind"] for s in data["sources"]}


# --------------------------------------------------------------- available_sources
def test_available_sources_lists_kill_clips_then_recordings(kill_dir, stubs, monkeypatch):
    (kill_dir / "k1.mp4").write_bytes(b"x")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: {
        "deadbeef": {**REC_GROUPS["deadbeef"], "has_file": True}})
    out = dataset.available_sources()
    assert out[0]["kind"] == "kill_clip" and "clipes_kill" in out[0]["file"]
    assert out[-1]["kind"] == "gravacao"


def test_available_sources_includes_review_frames(frames_dir, kill_dir, stubs, monkeypatch):
    _touch(frames_dir / "kill" / "gt_aaaaaaaaaaaa_f0000010.jpg")
    _touch(frames_dir / "nada" / "gt_bbbbbbbbbbbb_f0000000.jpg")
    _touch(frames_dir / "nada" / "gt_bbbbbbbbbbbb_f0000005.jpg")
    monkeypatch.setattr(dataset, "_cut_groups", lambda: {})
    out = dataset.available_sources()
    fr = [s for s in out if s["kind"] == "frame_review"][0]
    assert fr["pos"] == 1 and fr["neg"] == 2
