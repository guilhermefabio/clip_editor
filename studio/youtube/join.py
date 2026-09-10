"""Junta features editoriais (do Short) + features do YouTube (dos snapshots)
numa tabela por Short, pronta para regressão / classificação / ranking / séries
temporais. **Não treina nada** — só monta os dados.

Colunas por linha::

    short_id, video_id, duration_seconds, is_short
    ed_*   -> features editoriais (estrutura do edicao.json + features visuais
              do próprio Short quando o cache existir)
    yt_*   -> métricas por janela (24h/72h/7d) + crescimento
    target_quality_score, target_* -> alvo experimental (pesos configuráveis)
    *_version -> carimbo do pipeline que produziu o Short
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as studio_cfg  # noqa: E402
from pipeline import derive  # noqa: E402
from youtube import features as yt_features, links, storage  # noqa: E402

ROOT = studio_cfg.ROOT
WINDOWS = ("24h", "72h", "7d")


def _short_editorial(short: dict) -> dict:
    """Estrutura do edicao.json + features visuais do Short (cache _short)."""
    folder, name = short["short_key"].split("/", 1)
    plan_path = ROOT / folder / "projeto" / "edicao.json"
    out = {"ed_n_cuts": None, "ed_total_beats": None, "ed_n_replays": None,
           "ed_has_speedup": None, "ed_mean_gamma": None}
    try:
        d = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        edits = d.get("edits", []) if isinstance(d, dict) else d
        e = next((x for x in edits if isinstance(x, dict) and x.get("name") == name), None)
        if e:
            cuts = e.get("cuts", [])
            out.update(
                ed_n_cuts=len(cuts),
                ed_total_beats=sum(c.get("beats", 0) for c in cuts),
                ed_n_replays=sum(1 for c in cuts if c.get("replay")),
                ed_has_speedup=any((c.get("speed", 1) or 1) > 1.05 for c in cuts),
                ed_mean_gamma=round(float(np.mean([c.get("gamma", 1.08) for c in cuts])), 4) if cuts else None,
            )
    except (json.JSONDecodeError, OSError, StopIteration):
        pass

    mp4 = Path(short["mp4"])
    npz = _find_short_cache(mp4)
    if npz is not None:
        d = np.load(npz, allow_pickle=True)
        X, names = derive.augment(d["times"], d["X"], list(d["names"]), 3.0)
        col = {n: X[:, i] for i, n in enumerate(names)}
        out.update(
            ed_enemy_count=round(float(np.nanmean(col.get("person_count", [np.nan]))), 3),
            ed_enemy_peak=round(float(np.nanmax(col.get("person_count_wmax", [np.nan]))), 3),
            ed_movement_score=round(float(np.nanmean(col.get("center_motion", [np.nan]))), 4),
            ed_shot_flash_score=round(float(np.nanmax(col.get("flash_frac_wmax", [np.nan]))), 4),
            ed_hit_red_score=round(float(np.nanmax(col.get("red_frac_wmax", [np.nan]))), 4),
        )
    return out


def _find_short_cache(mp4: Path):
    import hashlib
    try:
        with open(mp4, "rb") as f:
            sha = hashlib.file_digest(f, "sha256").hexdigest()
    except OSError:
        return None
    p = studio_cfg.CACHE / sha / "features_short.npz"
    return p if p.exists() else None


def _yt_by_window(conn, video_id: str) -> dict:
    snaps = {s["age_window"]: s for s in storage.snapshots_for(conn, video_id) if s["age_window"]}
    out: dict = {}
    for w in WINDOWS:
        s = snaps.get(w)
        if not s:
            continue
        der = json.loads(s["derived_json"]) if s["derived_json"] else {}
        out[f"yt_views_{w}"] = s["views"]
        out[f"yt_engaged_views_{w}"] = s["engaged_views"]
        out[f"yt_avg_view_percentage_{w}"] = s["average_view_percentage"]
        out[f"yt_likes_per_1000_{w}"] = der.get("likes_per_1000_views")
        out[f"yt_comments_per_1000_{w}"] = der.get("comments_per_1000_views")
        out[f"yt_subs_per_1000_{w}"] = der.get("subs_per_1000_views")
        out[f"yt_watch_percentage_{w}"] = der.get("watch_percentage")
    if snaps.get("24h") and snaps.get("72h"):
        g = yt_features.growth_between(
            {"views": snaps["24h"]["views"], "engaged_views": snaps["24h"]["engaged_views"],
             "video_age_hours": snaps["24h"]["video_age_hours"]},
            {"views": snaps["72h"]["views"], "engaged_views": snaps["72h"]["engaged_views"],
             "video_age_hours": snaps["72h"]["video_age_hours"]})
        out["yt_growth_24h_72h"] = g["views_growth_rate"]
        out["yt_engaged_growth_24h_72h"] = g["engaged_views_growth_rate"]
    return out


def _target(conn, video_id: str) -> dict:
    """Alvo experimental: quality_score do snapshot mais maduro disponível."""
    for w in ("7d", "72h", "24h"):
        s = storage.latest_snapshot(conn, video_id, w)
        if s and s["quality_json"]:
            q = json.loads(s["quality_json"])
            return {"target_quality_score": q.get("quality_score"),
                    "target_window": w,
                    **{f"target_{k}": v for k, v in (q.get("components") or {}).items()}}
    return {"target_quality_score": None, "target_window": None}


def build_dataset(conn=None) -> list[dict]:
    conn = conn or storage.connect()
    storage.init_db(conn)
    linked = storage.all_links(conn)
    videos = {v["video_id"]: v for v in storage.all_videos(conn)}
    rows = []
    for short in links.iter_local_shorts():
        link = linked.get(short["short_key"])
        if not link:
            continue
        vid = link["video_id"]
        v = videos.get(vid, {})
        row = {
            "short_id": short["short_key"],
            "video_id": vid,
            "duration_seconds": v.get("duration_seconds"),
            "is_short": v.get("is_short"),
            "link_confidence": link.get("confidence"),
            **_short_editorial(short),
            **_yt_by_window(conn, vid),
            **_target(conn, vid),
        }
        last = storage.latest_snapshot(conn, vid)
        if last:
            for k in ("editor_version", "detector_version", "ranking_model_version",
                      "render_config_version"):
                row[k] = last.get(k)
        rows.append(row)
    return rows


def to_csv(rows: list[dict], path: str | Path) -> Path:
    path = Path(path)
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    return path


if __name__ == "__main__":
    c = storage.connect()
    rows = build_dataset(c)
    out = to_csv(rows, Path(__file__).resolve().parent / "editorial_youtube_dataset.csv")
    print(f"{len(rows)} Shorts ligados -> {out}")
