"""Liga cada Short editado (``shorts_bodycam*/projeto/edicao.json``) ao seu
``video_id`` no YouTube, por semelhança de título/nome de arquivo. Overrides
manuais ficam em ``links.json`` e na tabela ``youtube_short_links``.
"""
from __future__ import annotations

import json
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as studio_cfg  # noqa: E402
from youtube import config as cfg, storage  # noqa: E402

ROOT = studio_cfg.ROOT


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return " ".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def iter_local_shorts() -> list[dict]:
    out = []
    plans = (list(ROOT.glob("shorts_bodycam*/projeto/edicao.json"))
             + list((ROOT / "cliping").glob("*/projeto/edicao.json")))
    for plan_path in sorted(set(plans)):
        try:
            d = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError):
            continue
        edits = d.get("edits", []) if isinstance(d, dict) else d
        folder = plan_path.parent.parent.name
        for e in edits:
            if not isinstance(e, dict) or "name" not in e:
                continue
            out.append({
                "short_key": f"{folder}/{e['name']}",
                "folder": folder,
                "name": e["name"],
                "title": e.get("title", ""),
                "tag": e.get("tag", ""),
                "mp4": str((plan_path.parent.parent / f"{e['name']}.mp4")),
            })
    return out


def _best_match(short: dict, videos: list[dict]) -> tuple[dict | None, float, str]:
    cand_title = _norm(short["title"])
    cand_name = _norm(short["name"].split("_", 1)[-1].replace("_", " "))
    best, best_score, how = None, 0.0, ""
    for v in videos:
        vt = _norm(v.get("title", ""))
        for probe, label in ((cand_title, "title"), (cand_name, "filename")):
            if not probe or not vt:
                continue
            score = SequenceMatcher(None, probe, vt).ratio()
            if probe in vt or vt in probe:
                score = max(score, 0.9)
            if score > best_score:
                best, best_score, how = v, score, label
    return best, round(best_score, 3), how


def load_overrides() -> dict[str, str]:
    if cfg.LINKS_JSON.exists():
        try:
            return json.loads(cfg.LINKS_JSON.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def auto_link(conn, *, min_confidence: float = 0.62, dry_run: bool = False) -> list[dict]:
    videos = storage.all_videos(conn)
    existing = storage.all_links(conn)
    overrides = load_overrides()
    report = []
    for short in iter_local_shorts():
        key = short["short_key"]
        if key in overrides:
            if not dry_run:
                storage.set_link(conn, key, overrides[key], "manual", 1.0)
            report.append({"short_key": key, "video_id": overrides[key],
                           "matched_by": "manual", "confidence": 1.0})
            continue
        if key in existing and existing[key]["matched_by"] == "manual":
            continue
        v, score, how = _best_match(short, videos)
        if v and score >= min_confidence:
            if not dry_run:
                storage.set_link(conn, key, v["video_id"], how, score)
            report.append({"short_key": key, "video_id": v["video_id"],
                           "matched_by": how, "confidence": score,
                           "video_title": v.get("title")})
        else:
            report.append({"short_key": key, "video_id": None,
                           "confidence": score, "note": "sem correspondência confiável"})
    return report


if __name__ == "__main__":
    c = storage.connect()
    storage.init_db(c)
    for row in auto_link(c, dry_run="--apply" not in sys.argv):
        print(f"{row['short_key']:45s} -> {row.get('video_id') or '—':13s} "
              f"{row.get('matched_by', ''):9s} {row.get('confidence', 0)}")
