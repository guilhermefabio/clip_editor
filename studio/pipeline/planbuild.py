"""Write a harness-compatible plan from the UI's edits and validate it."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402

try:
    import versions as _versions  # studio-level version stamp
except Exception:  # noqa: BLE001
    _versions = None

PRIVATE = ("_peak", "_score", "_thumb", "_entry_beats", "_beats")


def next_lote_name() -> str:
    """Return the plan ``output`` for the next lote, e.g. ``cliping/lote7``."""
    n = 1
    for folder in list(C.CLIPING_DIR.glob("lote*")) + list(C.ROOT.glob("shorts_bodycam_lote*")):
        m = re.match(r"(?:shorts_bodycam_)?lote(\d+)$", folder.name)
        if m:
            n = max(n, int(m.group(1)) + 1)
    return f"{C.CLIPING_DIR.name}/lote{n}"


def _clean_edit(e: dict) -> dict:
    out = {k: v for k, v in e.items() if not k.startswith("_") and k not in PRIVATE}
    if isinstance(out.get("music"), dict):
        out["music"] = _fill_sha(out["music"])
    cuts = []
    for c in e["cuts"]:
        cc = {k: v for k, v in c.items() if not k.startswith("_")}
        if cc.get("file"):
            cc["file"] = C.rel_source(cc["file"])   # -> "gravacoes/x.mp4" quando for o caso
        cuts.append(cc)
    out["cuts"] = cuts
    return out


def _fill_sha(m: dict) -> dict:
    m = dict(m)
    if not m.get("sha256"):
        p = C.find_source(m["file"])
        with open(p, "rb") as f:
            m["sha256"] = __import__("hashlib").file_digest(f, "sha256").hexdigest()
    m.pop("duration", None)
    m.pop("known", None)
    return m


def build_plan(source_file: str, edits: list[dict], output: str | None = None,
               music: dict | None = None) -> dict:
    defaults = json.loads((C.HARNESS / "defaults.json").read_text(encoding="utf-8-sig"))
    output = output or next_lote_name()
    plan_music = _fill_sha(music) if music else defaults["music"]
    plan = {
        "version": 1,
        "sources": [C.rel_source(source_file)],
        "output": output,
        "channel": defaults["channel"],
        "game": defaults["game"],
        "batch_size": len(edits),
        "duration_range": [15, 20],
        "music": plan_music,
        "allow_reuse": False,
        "edits": [_clean_edit(e) for e in edits],
    }
    if _versions is not None:
        try:
            plan["versions"] = _versions.stamp()
        except Exception:  # noqa: BLE001
            pass
    plan_path = C.HARNESS / f"plano_{Path(output).name}.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    return {"plan_path": str(plan_path.relative_to(C.ROOT)), "output": output}


def check(plan_rel: str) -> dict:
    p = subprocess.run(
        [sys.executable, str(C.HARNESS / "shorts.py"), "check", plan_rel],
        cwd=C.ROOT, capture_output=True, text=True)
    return {"ok": p.returncode == 0,
            "message": (p.stdout + p.stderr).strip()}


if __name__ == "__main__":
    print(next_lote_name())
