"""Resolve local media tools before falling back to PATH."""
from pathlib import Path
import shutil


def resolve_tool(name: str, root: Path | None = None) -> Path:
    root = root or Path(__file__).resolve().parents[1]
    for filename in (name + ".exe", name):
        candidate = root / "_tools" / filename
        if candidate.is_file():
            return candidate
    found = shutil.which(name)
    if found:
        return Path(found)
    raise FileNotFoundError(
        f"{name} not found. Install FFmpeg/FFprobe in {root / '_tools'} "
        "or add their directory to PATH.")
