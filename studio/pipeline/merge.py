"""Join recordings into a new source before analysis; never change originals."""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import uuid
from fractions import Fraction
from pathlib import Path

import config as C


def resolve_sources(files: list[str]) -> list[Path]:
    if len(files) < 2:
        raise ValueError("Selecione pelo menos dois vídeos.")
    paths = []
    for name in files:
        p = C.find_source(name).resolve()
        if p.parent not in (C.ROOT.resolve(), C.GRAVACOES_DIR.resolve()):
            raise ValueError("Use vídeos da raiz ou de gravacoes/.")
        if not p.is_file() or p.suffix.lower() not in (".mp4", ".mkv", ".mov"):
            raise ValueError(f"Vídeo inválido: {name}")
        if p in paths:
            raise ValueError("O mesmo vídeo foi selecionado duas vezes.")
        paths.append(p)
    return paths


def probe(path: Path) -> dict:
    result = subprocess.run([str(C.FFPROBE), "-v", "error", "-show_streams",
                             "-show_format", "-of", "json", str(path)],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def original_cut(file: str, start: float, duration: float) -> tuple[str, float]:
    """Translate a joined timestamp back to an original, including nested joins."""
    visited = set()
    while True:
        source = C.find_source(file)
        manifest = source.with_suffix(".origens.json")
        if not manifest.exists():
            return C.rel_source(file), start
        if source in visited:
            raise ValueError("Mapa de origens circular.")
        visited.add(source)
        segments = json.loads(manifest.read_text(encoding="utf8"))["segments"]
        segment = next((s for s in segments if s["start"] <= start < s["start"] + s["duration"]), None)
        if segment is None or start + duration > segment["start"] + segment["duration"] + 1e-6:
            raise ValueError("Um corte atravessa a união de duas gravações. Ajuste seu início ou duração antes de gerar o plano.")
        file, start = segment["file"], round(start - segment["start"], 9)
        path = C.find_source(file)
        if not path.is_file():
            raise ValueError(f"Gravação original ausente: {file}")


def join(files: list[str], progress=lambda p, m: None) -> dict:
    paths = resolve_sources(files)
    records = []
    hashes = set()
    for i, path in enumerate(paths):
        progress(0.02 * i / len(paths), f"Conferindo {path.name}")
        with path.open("rb") as f:
            sha = hashlib.file_digest(f, "sha256").hexdigest()
        if sha in hashes:
            raise ValueError("Há vídeos duplicados pelo conteúdo na seleção.")
        hashes.add(sha)
        meta = probe(path)
        video = next(s for s in meta["streams"] if s["codec_type"] == "video")
        duration = float(meta["format"]["duration"])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError(f"Duração inválida: {path.name}")
        records.append((path, sha, meta, video, duration))

    first = records[0][3]
    width, height = int(first["width"]), int(first["height"])
    width += width % 2
    height += height % 2
    fps = Fraction(first.get("avg_frame_rate") or "0/1")
    if fps <= 0:
        fps = Fraction(first["r_frame_rate"])
    fps = min(fps, Fraction(60))
    if fps <= 0:
        raise ValueError("FPS inválido.")
    name = "unidos_" + uuid.uuid4().hex
    work = C.GRAVACOES_DIR / ("." + name)
    work.mkdir()
    dest = C.GRAVACOES_DIR / (name + ".mp4")
    manifest = dest.with_suffix(".origens.json")
    segments = []
    offset = 0.0

    def run(args):
        p = subprocess.run([str(C.FFMPEG), "-hide_banner", "-v", "error", "-nostdin", "-n",
                            *args], capture_output=True, text=True)
        if p.returncode:
            raise RuntimeError(p.stderr[-3000:] or "Falha ao unir vídeos.")

    try:
        for i, (path, sha, meta, video, duration) in enumerate(records):
            progress(0.02 + 0.83 * i / len(records), f"Preparando vídeo {i + 1}/{len(records)}")
            frames = round(duration * float(fps))
            duration = frames / float(fps)
            has_audio = any(s["codec_type"] == "audio" for s in meta["streams"])
            args = ["-i", str(path)]
            if not has_audio:
                args += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            vf = (f"setpts=PTS-STARTPTS,scale={width}:{height}:force_original_aspect_ratio=decrease,"
                  f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},"
                  f"tpad=stop_mode=clone:stop_duration=1,trim=duration={duration}")
            args += ["-map", "0:v:0", "-map", "0:a:0" if has_audio else "1:a:0",
                     "-vf", vf, "-af", "aresample=48000:async=1:first_pts=0,apad",
                     "-t", str(duration), "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                     "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
                     str(work / f"{i}.mkv")]
            run(args)
            segments.append({"file": path.relative_to(C.ROOT).as_posix(), "sha256": sha,
                             "start": offset, "duration": duration})
            offset += duration
        listing = work / "inputs.txt"
        listing.write_text("".join(f"file '{i}.mkv'\n" for i in range(len(records))), encoding="utf8")
        progress(0.87, "Unindo vídeo e áudio")
        pending = work / "joined.mp4"
        run(["-f", "concat", "-safe", "1", "-i", str(listing), "-c:v", "copy",
             "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", str(pending)])
        progress(0.95, "Validando arquivo unido")
        run(["-xerror", "-i", str(pending), "-f", "null", "-"])
        actual = float(probe(pending)["format"]["duration"])
        if abs(actual - offset) > max(0.25, len(records) / float(fps)):
            raise ValueError("A duração do vídeo unido divergiu da soma das fontes.")
        manifest.write_text(json.dumps({"version": 1, "segments": segments},
                                       ensure_ascii=False, indent=2), encoding="utf8")
        pending.rename(dest)
        return {"file": dest.name, "duration": actual,
                "manifest": manifest.relative_to(C.ROOT).as_posix()}
    finally:
        # Only files created in this uniquely named work directory.
        for item in work.iterdir():
            item.unlink()
        work.rmdir()
        if not dest.exists() and manifest.exists():
            manifest.unlink()
