"""Harvest training rows for the interest scorer.

All supervision is **raw gameplay** now (no rendered Shorts, no music):

1. **Kill clips** (``clipes_kill/*.mp4``) — 10-15 s cut straight from a
   recording around a kill, no edit. Every sampled frame is a positive. Same
   domain as the footage the model scores; the gunshot audio is intact.
2. **Raw recordings** (``*/projeto/edicao.json``) — positives = frames inside an
   approved cut; negatives = frames well outside every cut of the same
   recording (walking, menu, loot, dead time). Works from the source file OR
   its cached features, so a deleted recording still trains.

``groups`` carries the clip name / recording SHA so cross-source CV is honest.
Audio bands always stay in.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from pipeline import derive, features  # noqa: E402

GUARD_S = 2.0
NEG_RATIO = 3.0
CLIP_EDGE_S = 0.5          # descarta o começo/fim do clipe de kill (transição)
SEED = 20260907

SHORT_RE = re.compile(r"^\d{2,}_[A-Z0-9_]+\.mp4$")  # usado por training_status()


def _sha_for_file(name: str) -> str | None:
    p = C.find_source(name)
    if p.exists():
        try:
            return features.sha256(p)
        except OSError:
            return None
    return None


def _cut_groups() -> dict[str, dict]:
    """Group every approved cut by source SHA. Usable if the feature cache OR
    the source file is present -- a deleted recording still trains from cache.

    Returns {sha: {file, sha, intervals:[(start,end)], has_cache, has_file}}.
    """
    groups: dict[str, dict] = {}
    plans = list(C.ROOT.glob("*/projeto/edicao.json")) + list(C.CLIPING_DIR.glob("*/projeto/edicao.json"))
    for plan_path in sorted(set(plans)):
        try:
            d = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError):
            continue
        edits = d.get("edits", []) if isinstance(d, dict) else d
        for e in edits:
            if not isinstance(e, dict):
                continue
            for c in e.get("cuts", []):
                if not isinstance(c, dict) or "file" not in c:
                    continue
                sha = str(c.get("sha256") or "").lower() or _sha_for_file(c["file"])
                if not sha:
                    continue
                start = float(c["start"])
                end = float(c.get("end", start + float(c.get("duration", 0)) * float(c.get("speed", 1))))
                if end <= start:
                    continue
                g = groups.setdefault(sha, {
                    "file": c["file"], "sha": sha, "intervals": [],
                    "has_cache": (C.CACHE / sha / "features.npz").exists(),
                    "has_file": C.find_source(c["file"]).exists(),
                })
                g["intervals"].append((start, end))
    return groups


def iter_kill_clips() -> list[tuple[Path, str]]:
    """(mp4_path, group_id) for every raw kill clip in ``clipes_kill/``.

    Any ``.mp4`` counts; clips shorter/longer than the configured kill window
    are skipped with a note (probably not a kill clip).
    """
    folder = C.KILL_CLIPS_DIR
    if not folder.is_dir():
        return []
    out = []
    for mp4 in sorted(folder.glob("*.mp4")):
        try:
            dur = features.source_meta(mp4)["duration"]
        except Exception:  # noqa: BLE001
            dur = None
        if dur is not None and not (C.KILL_CLIP_MIN_S <= dur <= C.KILL_CLIP_MAX_S):
            print(f"  {mp4.name}: {dur:.1f}s fora de "
                  f"{C.KILL_CLIP_MIN_S:.0f}-{C.KILL_CLIP_MAX_S:.0f}s — ignorado")
            continue
        out.append((mp4, f"kill:{mp4.stem}"))
    return out


def available_sources() -> list[dict]:
    """Everything that can train the model right now."""
    out = []
    clips = iter_kill_clips()
    for mp4, _ in clips:
        out.append({"file": f"{C.KILL_CLIPS_DIR.name}/{mp4.name}", "kind": "kill_clip",
                    "cuts": 1, "seconds": None, "cached_only": False})
    for g in _cut_groups().values():
        if not (g["has_cache"] or g["has_file"]):
            continue
        out.append({
            "file": g["file"], "kind": "gravacao", "cuts": len(g["intervals"]),
            "seconds": round(sum(e - s for s, e in g["intervals"]), 1),
            "cached_only": g["has_cache"] and not g["has_file"],
        })
    return out


def training_status() -> dict:
    """Per-lote: contributing, or blocked on a missing raw recording."""
    groups = _cut_groups()
    lotes = []
    plans = (list(C.ROOT.glob("shorts_bodycam*/projeto/edicao.json"))
             + list(C.CLIPING_DIR.glob("*/projeto/edicao.json")))
    for plan_path in sorted(set(plans)):
        folder = plan_path.parent.parent.name
        try:
            d = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError):
            continue
        edits = d.get("edits", []) if isinstance(d, dict) else d
        shas = {str(c.get("sha256") or "").lower()
                for e in edits if isinstance(e, dict)
                for c in e.get("cuts", []) if isinstance(c, dict)}
        shas.discard("")
        blocked = sorted({groups[s]["file"] for s in shas
                          if s in groups and not (groups[s]["has_cache"] or groups[s]["has_file"])})
        ok = sorted({groups[s]["file"] for s in shas
                     if s in groups and (groups[s]["has_cache"] or groups[s]["has_file"])})
        mp4s = sum(1 for m in (plan_path.parent.parent).glob("*.mp4") if SHORT_RE.match(m.name))
        lotes.append({"lote": folder, "cuts_sources_ok": ok, "cuts_sources_missing": blocked,
                      "rendered_shorts": mp4s})
    return {"lotes": lotes}


def build(progress=None, use_kill_clips: bool = True):
    """Rows for the scorer.

    ``use_kill_clips`` (default True): kill clips in ``clipes_kill/`` are extra
    positives on top of the recordings. ``False`` = recordings only (the old
    ``--raw-only``). Either way the negatives come from the recordings and the
    audio bands stay in.
    """
    clips = iter_kill_clips() if use_kill_clips else []
    groups_meta = {sha: g for sha, g in _cut_groups().items()
                   if g["has_cache"] or g["has_file"]}
    if not groups_meta and not clips:
        raise RuntimeError(
            "Sem fontes de treino. Traga uma gravacao com cortes aprovados "
            f"(projeto/edicao.json) para a raiz e/ou clipes de kill em "
            f"{C.KILL_CLIPS_DIR.name}/.")
    if not groups_meta:
        raise RuntimeError(
            "Ha clipes de kill, mas nenhuma gravacao bruta com cortes aprovados "
            "(nem cache) para servir de NEGATIVO. Mantenha ao menos uma gravacao "
            "com projeto/edicao.json na raiz do BODYCAM.")
    total_units = len(groups_meta) + len(clips)

    rng = np.random.default_rng(SEED)
    Xs, ys, groups, tstamps = [], [], [], []
    names = None
    src_stats = []
    step = 0

    # 1) raw recordings: positives inside cuts, negatives well outside
    for sha, g in sorted(groups_meta.items()):
        name = Path(g["file"]).name
        if progress:
            progress(step / max(1, total_units), f"features {name}")
        step += 1
        f = features.load_cached(sha)
        src = C.find_source(g["file"])
        if f is None or (f.get("version", 0) < features.CACHE_VERSION and src.exists()):
            # cache velho + arquivo no disco: re-extrai p/ ter as features de kill
            f = features.extract(src)
        t = f["times"]
        Xa, names = derive.augment(t, f["X"], f["names"], C.FPS_ANALYSIS)
        pos = np.zeros(len(t), bool)
        guarded = np.zeros(len(t), bool)
        for s, e in g["intervals"]:
            pos |= (t >= s) & (t < e)
            guarded |= (t >= s - GUARD_S) & (t < e + GUARD_S)
        pos_idx = np.where(pos)[0]
        neg_pool = np.where(~guarded)[0]
        n_neg = min(len(neg_pool), int(len(pos_idx) * NEG_RATIO)) if len(pos_idx) else len(neg_pool)
        neg_idx = rng.choice(neg_pool, size=n_neg, replace=False) if n_neg else np.array([], int)
        keep = np.concatenate([pos_idx, neg_idx])
        Xs.append(Xa[keep])
        ys.append(np.concatenate([np.ones(len(pos_idx)), np.zeros(len(neg_idx))]))
        groups.append(np.full(len(keep), f["sha"][:12]))
        tstamps.append(t[keep])
        cached_only = g["has_cache"] and not g["has_file"]
        src_stats.append({"file": name, "kind": "gravacao", "pos": int(len(pos_idx)),
                          "neg": int(len(neg_idx)), "cached_only": cached_only})
        print(f"  {name}: {len(pos_idx)} pos / {len(neg_idx)} neg{'  (cache)' if cached_only else ''}")

    # 2) kill clips: every sampled frame (minus the transition edges) is positive
    for mp4, gid in clips:
        if progress:
            progress(step / max(1, total_units), f"kill {mp4.name}")
        step += 1
        try:
            f = features.extract(mp4, use_yolo=True)
        except Exception as exc:  # noqa: BLE001
            print(f"  {mp4.name}: falhou ({exc})")
            continue
        t = f["times"]
        if len(t) == 0:
            continue
        Xa, names = derive.augment(t, f["X"], f["names"], C.FPS_ANALYSIS)
        keep = np.where((t >= CLIP_EDGE_S) & (t <= t[-1] - CLIP_EDGE_S))[0]
        if len(keep) < 3:
            keep = np.arange(len(t))
        Xs.append(Xa[keep])
        ys.append(np.ones(len(keep)))
        groups.append(np.full(len(keep), gid[:24]))
        tstamps.append(t[keep])
        src_stats.append({"file": mp4.name, "kind": "kill_clip",
                          "pos": int(len(keep)), "neg": 0})
        print(f"  {mp4.name}: {len(keep)} pos (kill clip)")

    if not Xs:
        raise RuntimeError("Sem dados de treino apos ler as fontes.")

    X = np.vstack(Xs)
    y = np.concatenate(ys)
    if y.min() == y.max():
        raise RuntimeError(
            "So ha exemplos de uma classe. Precisa de ao menos uma gravacao com "
            "cortes aprovados (positivos) E trecho fora dos cortes (negativos).")
    if progress:
        progress(1.0, f"{len(y)} linhas")
    return {
        "X": X, "y": y, "groups": np.concatenate(groups),
        "names": names, "times": np.concatenate(tstamps), "sources": src_stats,
    }


if __name__ == "__main__":
    import json as _j
    if "--status" in sys.argv:
        print(_j.dumps(training_status(), ensure_ascii=False, indent=2))
    else:
        d = build(progress=lambda p, m: print(f"  {p*100:5.1f}%  {m}"),
                  use_kill_clips="--no-kill-clips" not in sys.argv)
        ns = len({g for g in d["groups"]})
        print(f"\n{len(d['y'])} rows, {d['X'].shape[1]} features, "
              f"{int(d['y'].sum())} positivos, {ns} grupos")
