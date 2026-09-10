"""Local web studio: analyse a gameplay recording with the trained scorer,
assemble shorts in the approved pattern, render them through the existing
harness, and review the results. No LLM in the loop.

Run:  python studio/app.py      then open http://127.0.0.1:8765
"""
from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
from pipeline import beatgrid, features, group, media, planbuild, score  # noqa: E402

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel  # noqa: E402
import uvicorn  # noqa: E402

app = FastAPI(title="BODYCAM Studio")
JOBS: dict[str, dict] = {}
IDX = C.CACHE / "sources.json"


# ----------------------------------------------------------------- job helper
def start_job(kind: str, fn) -> str:
    jid = uuid.uuid4().hex[:8]
    JOBS[jid] = {"kind": kind, "progress": 0.0, "message": "iniciando",
                 "status": "running", "result": None, "log": []}

    def prog(p, m):
        JOBS[jid]["progress"] = round(float(p), 3)
        JOBS[jid]["message"] = str(m)

    def worker():
        try:
            JOBS[jid]["result"] = fn(prog, JOBS[jid]["log"])
            JOBS[jid]["status"] = "done"
            JOBS[jid]["progress"] = 1.0
        except Exception as exc:  # noqa: BLE001
            JOBS[jid]["status"] = "error"
            JOBS[jid]["message"] = f"{type(exc).__name__}: {exc}"

    threading.Thread(target=worker, daemon=True).start()
    return jid


@app.get("/api/job/{jid}")
def job(jid: str):
    if jid not in JOBS:
        raise HTTPException(404)
    return JOBS[jid]


# ----------------------------------------------------------------- sources
def _source_index() -> dict:
    return json.loads(IDX.read_text(encoding="utf8")) if IDX.exists() else {}


def _save_index(d: dict):
    IDX.write_text(json.dumps(d), encoding="utf8")


@app.get("/api/sources")
def sources():
    idx = _source_index()
    out = []
    seen = set()
    cands = list(C.GRAVACOES_DIR.glob("*.m*")) + list(C.ROOT.glob("*.m*"))
    for p in sorted(cands, key=lambda q: q.name):
        if p.suffix.lower() not in (".mkv", ".mp4", ".mov") or p.stat().st_size < 20_000_000:
            continue
        if p.name in seen:
            continue
        seen.add(p.name)
        st = p.stat()
        key = f"{p.name}:{st.st_size}:{int(st.st_mtime)}"
        rec = idx.get(key)
        if not rec:
            try:
                m = features.source_meta(p)
                rec = {"sha": features.sha256(p), "duration": m["duration"],
                       "width": m["width"], "height": m["height"]}
            except Exception:  # noqa: BLE001
                continue
            idx[key] = rec
        scored = (C.CACHE / rec["sha"] / "score.json").exists()
        out.append({"file": p.name, "size_mb": round(st.st_size / 1e6, 1),
                    "duration": rec["duration"], "sha": rec["sha"], "scored": scored})
    _save_index(idx)
    return out


# ----------------------------------------------------------------- model
@app.get("/api/model")
def model_info():
    from pipeline import dataset
    try:
        avail = dataset.available_sources()
    except Exception:  # noqa: BLE001
        avail = []
    try:
        status = dataset.training_status()
    except Exception:  # noqa: BLE001
        status = {"lotes": []}
    meta_path = C.MODEL_DIR / "scorer_meta.json"
    base = {"trainable": bool(avail), "train_sources_on_disk": avail,
            "training_status": status}
    if not meta_path.exists():
        return {"trained": False, **base}
    return {"trained": True, **base, **json.loads(meta_path.read_text(encoding="utf8"))}


class TrainBody(BaseModel):
    raw_only: bool = False


@app.post("/api/train")
def train(body: TrainBody | None = None):
    from pipeline import train as trainmod
    raw_only = bool(body.raw_only) if body else False
    return {"job": start_job(
        "train", lambda prog, log: trainmod.train(progress=prog, raw_only=raw_only))}


# ----------------------------------------------------------------- music
@app.get("/api/music")
def music_list():
    return beatgrid.registry()


class MusicBody(BaseModel):
    file: str


@app.post("/api/music/analyze")
def music_analyze(body: MusicBody):
    p = C.ROOT / body.file
    if not p.exists():
        raise HTTPException(404)
    return {"job": start_job("beat", lambda prog, log: beatgrid.estimate(p))}


# ----------------------------------------------------------------- analyse
class FileBody(BaseModel):
    file: str
    force: bool = False


@app.post("/api/analyze")
def analyze(body: FileBody):
    src = C.find_source(body.file)
    if not src.exists():
        raise HTTPException(404, "arquivo nao encontrado")

    def run(prog, log):
        r = score.score_source(src, progress=prog, force=body.force)
        return {"file": r["file"], "sha": r["sha"], "frames": len(r["times"]),
                "max_score": max(r["smooth"], default=0), "threshold": r["threshold"]}

    return {"job": start_job("analyze", run)}


@app.get("/api/score")
def get_score(file: str):
    src = C.find_source(file)
    if not src.exists():
        raise HTTPException(404)
    sha = _sha_for(file)
    sc_path = C.CACHE / sha / "score.json"
    if not sc_path.exists():
        raise HTTPException(409, "ainda nao analisado")
    sc = json.loads(sc_path.read_text(encoding="utf8"))
    cand = group.candidates(sc)
    return {"score": sc, "candidates": cand}


class GroupBody(BaseModel):
    file: str
    batch_size: int = 5
    cuts_per: int = C.DEFAULT_CUTS_PER_SHORT
    music: dict | None = None
    entry_beats: int = 0
    spread: float | None = None


@app.post("/api/group")
def make_groups(body: GroupBody):
    sha = _sha_for(body.file)
    sc_path = C.CACHE / sha / "score.json"
    if not sc_path.exists():
        raise HTTPException(409, "ainda nao analisado")
    sc = json.loads(sc_path.read_text(encoding="utf8"))
    cand = group.candidates(sc)
    return group.autogroup(sc, cand, batch_size=body.batch_size, cuts_per=body.cuts_per,
                           music=body.music, entry_beats=body.entry_beats,
                           spread=body.spread)


# ----------------------------------------------------------------- frames
@app.get("/api/frame")
def frame(file: str, t: float, w: int = 380):
    src = C.find_source(file)
    if not src.exists():
        raise HTTPException(404)
    sha = _sha_for(file)
    dest = C.CACHE / sha / "frames" / f"{t:.2f}_{w}.jpg"
    media.frame_jpeg(src, t, dest, width=w)
    return FileResponse(dest)


# ----------------------------------------------------------------- plan + render
class PlanBody(BaseModel):
    file: str
    edits: list
    output: str | None = None
    music: dict | None = None


@app.post("/api/plan")
def make_plan(body: PlanBody):
    built = planbuild.build_plan(body.file, body.edits, body.output, music=body.music)
    verdict = planbuild.check(built["plan_path"])
    return {**built, **verdict}


class RenderBody(BaseModel):
    plan_path: str


@app.post("/api/render")
def render(body: RenderBody):
    plan_rel = body.plan_path
    plan_abs = (C.ROOT / plan_rel)
    if not plan_abs.exists():
        raise HTTPException(404, "plano nao encontrado")
    plan = json.loads(plan_abs.read_text(encoding="utf-8-sig"))
    total = len(plan["edits"])

    def run(prog, log):
        for phase, weight0, weight1 in (("render", 0.0, 0.8), ("verify", 0.8, 1.0)):
            prog(weight0, phase)
            proc = subprocess.Popen(
                [sys.executable, str(C.HARNESS / "shorts.py"), phase, plan_rel],
                cwd=C.ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            done = 0
            for line in proc.stdout:
                line = line.rstrip()
                log.append(line)
                if "PRONTO:" in line or '"file"' in line:
                    done += 1
                    prog(weight0 + (weight1 - weight0) * min(1.0, done / max(1, total)), line[:80])
            proc.wait()
            if proc.returncode:
                raise RuntimeError("\n".join(log[-12:]))
        return {"output": plan["output"], "batch": f"/api/batch/{plan['output']}"}

    return {"job": start_job("render", run)}


@app.get("/api/batch/{output:path}")
def batch(output: str):
    folder = (C.ROOT / output).resolve()
    if not folder.is_relative_to(C.ROOT) or not folder.is_dir():
        raise HTTPException(404)
    plan_path = folder / "projeto" / "edicao.json"
    edits = []
    if plan_path.exists():
        d = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        edits = d.get("edits", []) if isinstance(d, dict) else d
    loud = {}
    vpath = folder / "projeto" / "verificacao.json"
    if vpath.exists():
        for v in json.loads(vpath.read_text(encoding="utf8")).get("videos", []):
            loud[v["file"]] = v
    items = []
    for e in edits:
        name = e["name"]
        mp4 = folder / f"{name}.mp4"
        items.append({
            "name": name, "title": e.get("title", ""), "tag": e.get("tag", ""),
            "rendered": mp4.exists(),
            "video": f"/media/{output}/{name}.mp4" if mp4.exists() else None,
            "poster": f"/media/{output}/{name}.jpg" if (folder / f"{name}.jpg").exists() else None,
            "loudness": loud.get(f"{name}.mp4", {}).get("loudness_LUFS"),
        })
    return {"output": output, "items": items,
            "watch": f"/media/{output}/ASSISTIR.html" if (folder / "ASSISTIR.html").exists() else None}


@app.get("/media/{output:path}/{name}")
def media_file(output: str, name: str):
    p = (C.ROOT / output / name).resolve()
    if not p.is_relative_to(C.ROOT) or not p.exists():
        raise HTTPException(404)
    return FileResponse(p)


# ----------------------------------------------------------------- helpers / static
def _sha_for(file: str) -> str:
    idx = _source_index()
    p = C.find_source(file)
    st = p.stat()
    key = f"{p.name}:{st.st_size}:{int(st.st_mtime)}"
    if key in idx:
        return idx[key]["sha"]
    sha = features.sha256(p)
    idx[key] = {"sha": sha}
    _save_index(idx)
    return sha


@app.get("/", response_class=HTMLResponse)
def index():
    return (C.WEB / "index.html").read_text(encoding="utf8")


app.mount("/static", StaticFiles(directory=str(C.WEB)), name="static")


if __name__ == "__main__":
    print("BODYCAM Studio  ->  http://127.0.0.1:8765")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="warning")
