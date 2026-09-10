"""Carimbo de versão do pipeline que produziu cada Short.

Sem git nesta pasta, então cada versão é ``<semver manual>+<fingerprint>``:
o semver vem de ``studio/youtube/versions.json`` (você edita quando muda algo
de propósito) e o fingerprint é um hash curto dos arquivos que importam, para
detectar mudança silenciosa.

Guardado junto do plano/edição e replicado no snapshot de métricas, para depois
comparar decisões editoriais de versões diferentes.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as studio_cfg  # noqa: E402

ROOT = studio_cfg.ROOT
VERSIONS_JSON = Path(__file__).resolve().parent / "versions.json"

_COMPONENTS = {
    "editor_version": ["studio/pipeline/group.py", "studio/pipeline/planbuild.py",
                       "studio/pipeline/derive.py", "studio/config.py"],
    "detector_version": ["studio/pipeline/features.py", "studio/model/yolov8n.pt"],
    "ranking_model_version": ["studio/model/scorer.joblib", "studio/model/scorer_meta.json"],
    "render_config_version": ["harness/engine.py", "harness/defaults.json"],
}
_DEFAULT_SEMVER = {k: "0.1.0" for k in _COMPONENTS}


def _fingerprint(rel_paths: list[str]) -> str:
    h = hashlib.sha256()
    for rel in rel_paths:
        p = ROOT / rel
        if p.exists():
            h.update(rel.encode())
            with p.open("rb") as f:
                for block in iter(lambda: f.read(1 << 20), b""):
                    h.update(block)
    return h.hexdigest()[:10]


def _semver() -> dict:
    if VERSIONS_JSON.exists():
        try:
            data = json.loads(VERSIONS_JSON.read_text(encoding="utf-8"))
            return {**_DEFAULT_SEMVER, **{k: str(v) for k, v in data.items()}}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(_DEFAULT_SEMVER)


def stamp() -> dict:
    """{'editor_version': '0.1.0+ab12cd34ef', ...}"""
    sv = _semver()
    return {name: f"{sv[name]}+{_fingerprint(paths)}" for name, paths in _COMPONENTS.items()}


if __name__ == "__main__":
    print(json.dumps(stamp(), indent=2))
