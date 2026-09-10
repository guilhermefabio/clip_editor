"""Persistência em SQLite (stdlib). Sem ORM, sem framework de migração.

* ``youtube_videos``            — 1 linha por vídeo (upsert).
* ``youtube_metric_snapshots``  — **append puro**; cada coleta é um snapshot
  histórico datado, para estudar a curva de crescimento.
* ``youtube_short_links``       — Short editado  <->  video_id do YouTube.

O schema é criado on-demand por :func:`init_db`. Para evoluir: acrescente
colunas com ``ALTER TABLE`` em :func:`_migrate` (idempotente).
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from youtube import config as cfg  # noqa: E402
from youtube.util import utcnow  # noqa: E402

SCHEMA = """
CREATE TABLE IF NOT EXISTS youtube_videos (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  video_id          TEXT UNIQUE NOT NULL,
  title             TEXT,
  published_at      TEXT,
  duration_seconds  REAL,
  channel_id        TEXT,
  is_short          INTEGER,
  created_at        TEXT NOT NULL,
  updated_at        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS youtube_metric_snapshots (
  id                        INTEGER PRIMARY KEY AUTOINCREMENT,
  video_id                  TEXT NOT NULL,
  captured_at               TEXT NOT NULL,
  video_age_hours           REAL,
  age_window                TEXT,
  period_start              TEXT,
  period_end                TEXT,
  views                     INTEGER,
  engaged_views             INTEGER,
  estimated_minutes_watched REAL,
  average_view_duration     REAL,
  average_view_percentage   REAL,
  likes                     INTEGER,
  comments                  INTEGER,
  shares                    INTEGER,
  subscribers_gained        INTEGER,
  subscribers_lost          INTEGER,
  data_views                INTEGER,
  data_likes                INTEGER,
  data_comments             INTEGER,
  traffic_source            TEXT,
  creator_content_type      TEXT,
  unavailable_metrics       TEXT,
  derived_json              TEXT,
  quality_json              TEXT,
  editor_version            TEXT,
  detector_version          TEXT,
  ranking_model_version     TEXT,
  render_config_version     TEXT,
  created_at                TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_snap_video ON youtube_metric_snapshots(video_id, captured_at);
CREATE INDEX IF NOT EXISTS ix_snap_window ON youtube_metric_snapshots(video_id, age_window);

CREATE TABLE IF NOT EXISTS youtube_short_links (
  short_key   TEXT PRIMARY KEY,
  video_id    TEXT NOT NULL,
  matched_by  TEXT,
  confidence  REAL,
  updated_at  TEXT NOT NULL
);
"""

_SNAP_COLS = [
    "video_id", "captured_at", "video_age_hours", "age_window", "period_start",
    "period_end", "views", "engaged_views", "estimated_minutes_watched",
    "average_view_duration", "average_view_percentage", "likes", "comments",
    "shares", "subscribers_gained", "subscribers_lost", "data_views",
    "data_likes", "data_comments", "traffic_source", "creator_content_type",
    "unavailable_metrics", "derived_json", "quality_json", "editor_version",
    "detector_version", "ranking_model_version", "render_config_version",
]


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path or cfg.DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    _migrate(conn)
    conn.commit()


def _migrate(conn: sqlite3.Connection) -> None:
    """Acrescente colunas novas aqui; ignora se já existir."""
    have = {r[1] for r in conn.execute("PRAGMA table_info(youtube_metric_snapshots)")}
    for col, decl in []:  # ex: [("new_col", "TEXT")]
        if col not in have:
            conn.execute(f"ALTER TABLE youtube_metric_snapshots ADD COLUMN {col} {decl}")


# -- videos ---------------------------------------------------------------
def upsert_video(conn: sqlite3.Connection, v: dict) -> None:
    now = _iso(utcnow())
    conn.execute(
        """INSERT INTO youtube_videos
             (video_id,title,published_at,duration_seconds,channel_id,is_short,created_at,updated_at)
           VALUES (:video_id,:title,:published_at,:duration_seconds,:channel_id,:is_short,:now,:now)
           ON CONFLICT(video_id) DO UPDATE SET
             title=excluded.title, published_at=excluded.published_at,
             duration_seconds=excluded.duration_seconds, channel_id=excluded.channel_id,
             is_short=excluded.is_short, updated_at=excluded.updated_at""",
        {**{k: v.get(k) for k in
            ("video_id", "title", "published_at", "duration_seconds", "channel_id")},
         "is_short": int(bool(v.get("is_short"))) if v.get("is_short") is not None else None,
         "now": now},
    )
    conn.commit()


def all_videos(conn: sqlite3.Connection, *, shorts_only: bool = False) -> list[dict]:
    q = "SELECT * FROM youtube_videos"
    if shorts_only:
        q += " WHERE is_short=1"
    q += " ORDER BY published_at DESC"
    return [dict(r) for r in conn.execute(q)]


def get_video(conn: sqlite3.Connection, video_id: str) -> dict | None:
    r = conn.execute("SELECT * FROM youtube_videos WHERE video_id=?", (video_id,)).fetchone()
    return dict(r) if r else None


# -- snapshots ----------------------------------------------------------------
def insert_snapshot(conn: sqlite3.Connection, snap: dict) -> int:
    row = {c: snap.get(c) for c in _SNAP_COLS}
    for k in ("derived_json", "quality_json"):
        if isinstance(row.get(k), (dict, list)):
            row[k] = json.dumps(row[k], ensure_ascii=False)
    if isinstance(row.get("unavailable_metrics"), (list, tuple)):
        row["unavailable_metrics"] = ",".join(row["unavailable_metrics"])
    row["created_at"] = _iso(utcnow())
    cols = _SNAP_COLS + ["created_at"]
    cur = conn.execute(
        f"INSERT INTO youtube_metric_snapshots ({','.join(cols)}) "
        f"VALUES ({','.join(':' + c for c in cols)})", row)
    conn.commit()
    return cur.lastrowid


def snapshot_exists(conn: sqlite3.Connection, video_id: str, age_window: str) -> bool:
    r = conn.execute(
        "SELECT 1 FROM youtube_metric_snapshots WHERE video_id=? AND age_window=? LIMIT 1",
        (video_id, age_window)).fetchone()
    return r is not None


def snapshots_for(conn: sqlite3.Connection, video_id: str) -> list[dict]:
    return [dict(r) for r in conn.execute(
        "SELECT * FROM youtube_metric_snapshots WHERE video_id=? ORDER BY captured_at",
        (video_id,))]


def latest_snapshot(conn: sqlite3.Connection, video_id: str,
                    age_window: str | None = None) -> dict | None:
    q = "SELECT * FROM youtube_metric_snapshots WHERE video_id=?"
    args: list = [video_id]
    if age_window:
        q += " AND age_window=?"
        args.append(age_window)
    q += " ORDER BY captured_at DESC LIMIT 1"
    r = conn.execute(q, args).fetchone()
    return dict(r) if r else None


# -- links ------------------------------------------------------------------
def set_link(conn: sqlite3.Connection, short_key: str, video_id: str,
             matched_by: str = "manual", confidence: float = 1.0) -> None:
    conn.execute(
        """INSERT INTO youtube_short_links (short_key,video_id,matched_by,confidence,updated_at)
           VALUES (?,?,?,?,?)
           ON CONFLICT(short_key) DO UPDATE SET
             video_id=excluded.video_id, matched_by=excluded.matched_by,
             confidence=excluded.confidence, updated_at=excluded.updated_at""",
        (short_key, video_id, matched_by, confidence, _iso(utcnow())))
    conn.commit()


def all_links(conn: sqlite3.Connection) -> dict[str, dict]:
    return {r["short_key"]: dict(r) for r in conn.execute("SELECT * FROM youtube_short_links")}


def _iso(dt) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    c = connect()
    init_db(c)
    print("schema pronto em", cfg.DB_PATH)
    print("videos:", len(all_videos(c)), "| links:", len(all_links(c)))
