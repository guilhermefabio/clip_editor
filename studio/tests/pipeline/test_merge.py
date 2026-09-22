"""Real FFmpeg coverage of ordered joining, audio and original timestamps."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pipeline import merge


@pytest.fixture
def recordings(tmp_path, monkeypatch):
    monkeypatch.setattr(merge.C, "ROOT", tmp_path)
    monkeypatch.setattr(merge.C, "GRAVACOES_DIR", tmp_path / "gravacoes")
    merge.C.GRAVACOES_DIR.mkdir()
    for name, color, size, audio in [("a.mp4", "red", "160x90", True),
                                      ("b.mp4", "blue", "96x96", False)]:
        args = [str(merge.C.FFMPEG), "-v", "error", "-f", "lavfi", "-i",
                f"color={color}:s={size}:r=30:d=1"]
        if audio:
            args += ["-f", "lavfi", "-i", "sine=frequency=440:duration=1"]
        subprocess.run(args + ["-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                               str(tmp_path / name)], check=True)
    return tmp_path


def test_join_order_audio_and_mapping(recordings):
    result = merge.join(["a.mp4", "b.mp4"])
    output = merge.C.find_source(result["file"])
    meta = merge.probe(output)
    assert abs(result["duration"] - 2) < 0.15
    assert {s["codec_type"] for s in meta["streams"]} == {"video", "audio"}
    for t, channel in [(0.4, 0), (1.4, 2)]:
        frame = subprocess.check_output([str(merge.C.FFMPEG), "-v", "error", "-ss", str(t),
            "-i", str(output), "-vf", "scale=1:1", "-frames:v", "1", "-pix_fmt", "rgb24",
            "-f", "rawvideo", "-"])
        assert frame[channel] > 80
        assert frame[channel] > frame[2 - channel] * 3
    audio = subprocess.check_output([str(merge.C.FFMPEG), "-v", "error", "-ss", "1.3",
        "-i", str(output), "-t", "0.3", "-f", "s16le", "-ac", "1", "-"])
    import array
    samples = array.array("h", audio)
    assert max(abs(v) for v in samples) < 10
    assert merge.original_cut(result["file"], 1.2, 0.5) == ("b.mp4", 0.2)
    with pytest.raises(ValueError, match="atravessa"):
        merge.original_cut(result["file"], 0.8, 0.5)
    assert (recordings / "a.mp4").exists()
    assert not list(merge.C.GRAVACOES_DIR.glob(".unidos_*"))
    assert json.loads(output.with_suffix(".origens.json").read_text())["segments"][0]["file"] == "a.mp4"


def test_invalid_and_duplicate_content(recordings):
    with pytest.raises(ValueError):
        merge.resolve_sources(["a.mp4"])
    with pytest.raises(ValueError):
        merge.resolve_sources(["a.mp4", "a.mp4"])
    with pytest.raises(ValueError):
        merge.resolve_sources(["a.mp4", "missing.mp4"])
    (recordings / "copy.mp4").write_bytes((recordings / "a.mp4").read_bytes())
    with pytest.raises(ValueError, match="duplicados"):
        merge.join(["a.mp4", "copy.mp4"])
    assert not list(merge.C.GRAVACOES_DIR.iterdir())


def test_failure_removes_partial_files(recordings, monkeypatch):
    real_run = merge.subprocess.run
    def fail_encoding(args, **kwargs):
        if "-crf" in args:
            Path(args[-1]).write_bytes(b"partial")
            return subprocess.CompletedProcess(args, 1, "", "encoding failed")
        return real_run(args, **kwargs)
    monkeypatch.setattr(merge.subprocess, "run", fail_encoding)
    with pytest.raises(RuntimeError, match="encoding failed"):
        merge.join(["a.mp4", "b.mp4"])
    assert not list(merge.C.GRAVACOES_DIR.iterdir())


def test_plan_uses_original_files(recordings, monkeypatch):
    from pipeline import planbuild
    result = merge.join(["a.mp4", "b.mp4"])
    harness = recordings / "harness"
    harness.mkdir()
    monkeypatch.setattr(merge.C, "HARNESS", harness)
    music = {"file": "beat.wav", "sha256": "test", "bpm": 120}
    (harness / "defaults.json").write_text(json.dumps({
        "channel": "test", "game": "test", "music": music}))
    built = planbuild.build_plan(result["file"], [{"cuts": [
        {"file": result["file"], "start": 1.2, "beats": 1}]}], "cliping/lote1")
    plan = json.loads((recordings / built["plan_path"]).read_text())
    assert plan["sources"] == ["b.mp4"]
    assert plan["edits"][0]["cuts"][0]["start"] == 0.2
