"""Tiny helpers to pull still frames out of a source for the web UI."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402


def frame_jpeg(source: Path, t: float, dest: Path, width: int = 380) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest
    subprocess.run(
        [str(C.FFMPEG), "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", str(source),
         "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "3", "-y", str(dest)],
        check=True)
    return dest
