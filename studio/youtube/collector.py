"""Orquestra a coleta e a persistência dos snapshots.

Funções principais::

    collect_channel(conn, client)                       # descobre + grava os vídeos
    collect_video(video_id, ...)                        # dados básicos de 1 vídeo
    collect_all_recent_videos(conn, client, days=...)   # vídeos recentes + snapshots devidos
    collect_metrics_for_video(video_id, start, end, ..) # 1 snapshot de métricas
    snapshot_due_windows(video, conn, client)           # snapshots por idade (1h..28d)

CLI::

    python studio/youtube/collector.py init
    python studio/youtube/collector.py channel
    python studio/youtube/collector.py recent --days 45
    python studio/youtube/collector.py metrics <VIDEO_ID> --window 24h
    python studio/youtube/collector.py snapshot --all
    python studio/youtube/collector.py link --apply

Preparado para rodar por cron / APScheduler / Celery / GitHub Actions: cada
comando é idempotente onde faz sentido e não abre servidor nenhum.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import versions  # noqa: E402  (studio-level: carimbo do pipeline)
from youtube import analytics_api, data_api, features, storage, windows  # noqa: E402
from youtube import config as cfg  # noqa: E402
from youtube.errors import (  # noqa: E402
    AuthError, QuotaError, VideoUnavailableError, YouTubeError,
)
from youtube.log import E_SNAPSHOT, get_logger  # noqa: E402
from youtube.util import age_hours, iso, utcnow  # noqa: E402

log = get_logger("youtube.collector")


def _ctx(conn=None, client=None):
    if conn is None:
        conn = storage.connect()
        storage.init_db(conn)
    if client is None:
        from youtube.client import YouTubeClient
        client = YouTubeClient()
    return conn, client


# -- descoberta / dados básicos ------------------------------------------
def collect_channel(conn=None, client=None) -> dict:
    conn, client = _ctx(conn, client)
    ch = data_api.resolve_channel(client)
    ids = [x["video_id"] for x in data_api.list_channel_video_ids(client, ch["uploads_playlist_id"])]
    videos = data_api.get_videos(client, ids)
    for v in videos:
        storage.upsert_video(conn, v)
    missing = sorted(set(ids) - {v["video_id"] for v in videos})
    log.info("canal %s: %d vídeos gravados, %d indisponíveis",
             ch["channel_id"], len(videos), len(missing))
    return {"channel": ch, "saved": len(videos), "unavailable": missing}


def collect_video(video_id: str, conn=None, client=None) -> dict:
    conn, client = _ctx(conn, client)
    v = data_api.get_video(client, video_id)
    storage.upsert_video(conn, v)
    return v


# -- métricas -----------------------------------------------------------------
def collect_metrics_for_video(video_id: str, start_date=None, end_date=None, *,
                              age_window: str | None = None, shorts_segment: bool = True,
                              force: bool = False, conn=None, client=None) -> dict | None:
    conn, client = _ctx(conn, client)
    if age_window and not force and storage.snapshot_exists(conn, video_id, age_window):
        log.info("janela %s de %s já capturada; pulando (use --force)", age_window, video_id)
        return None

    video = storage.get_video(conn, video_id) or collect_video(video_id, conn, client)
    is_short = bool(video.get("is_short"))

    an = analytics_api.query_video(
        client, video_id, start_date=start_date, end_date=end_date,
        shorts_only=shorts_segment and is_short)
    raw = an["metrics"]
    traffic = analytics_api.query_traffic_sources(
        client, video_id, start_date=start_date, end_date=end_date)
    dominant_traffic = max(traffic, key=traffic.get) if traffic else None

    der = features.derived_metrics(raw)
    qual = features.quality_score(raw, der)
    ver = versions.stamp()

    snap = {
        "video_id": video_id,
        "captured_at": iso(utcnow()),
        "video_age_hours": age_hours(video.get("published_at")),
        "age_window": age_window,
        "period_start": an["period_start"],
        "period_end": an["period_end"],
        "views": raw.get("views"),
        "engaged_views": raw.get("engagedViews"),
        "estimated_minutes_watched": raw.get("estimatedMinutesWatched"),
        "average_view_duration": raw.get("averageViewDuration"),
        "average_view_percentage": raw.get("averageViewPercentage"),
        "likes": raw.get("likes"),
        "comments": raw.get("comments"),
        "shares": raw.get("shares"),
        "subscribers_gained": raw.get("subscribersGained"),
        "subscribers_lost": raw.get("subscribersLost"),
        "data_views": video.get("view_count"),
        "data_likes": video.get("like_count"),
        "data_comments": video.get("comment_count"),
        "traffic_source": dominant_traffic,
        "creator_content_type": an["creator_content_type"],
        "unavailable_metrics": an["unavailable_metrics"],
        "derived_json": der,
        "quality_json": qual,
        **ver,
    }
    sid = storage.insert_snapshot(conn, snap)
    log.info("%s id=%d video=%s janela=%s views=%s", E_SNAPSHOT, sid, video_id,
             age_window or "ad-hoc", raw.get("views"))
    return snap


def snapshot_due_windows(video: dict, conn=None, client=None, *, force=False) -> list[dict]:
    conn, client = _ctx(conn, client)
    vid = video["video_id"]
    captured = {s["age_window"] for s in storage.snapshots_for(conn, vid) if s["age_window"]}
    age = age_hours(video.get("published_at"))
    plan = windows.classify(age, set() if force else captured)
    if plan["missed"]:
        log.warning("video %s: janelas perdidas %s (idade %.1fh)", vid, plan["missed"], age or -1)

    done = []
    for w in plan["due"]:
        try:
            start, end = windows.window_date_range(video["published_at"], w)
            snap = collect_metrics_for_video(vid, start, end, age_window=w,
                                             force=force, conn=conn, client=client)
            if snap:
                done.append(snap)
        except (VideoUnavailableError, YouTubeError) as exc:
            log.error("video %s janela %s: %s", vid, w, exc)
    return done


def collect_all_recent_videos(conn=None, client=None, *, days: int = 45,
                              force: bool = False) -> dict:
    conn, client = _ctx(conn, client)
    collect_channel(conn, client)
    cutoff = utcnow().timestamp() - days * 86400
    from youtube.util import parse_rfc3339

    recent = [v for v in storage.all_videos(conn)
              if (parse_rfc3339(v.get("published_at")) or utcnow()).timestamp() >= cutoff]
    snaps, errors = 0, []
    for v in recent:
        try:
            snaps += len(snapshot_due_windows(v, conn, client, force=force))
        except QuotaError:
            log.error("quota excedida — interrompendo a coleta do canal")
            return {"videos": len(recent), "snapshots": snaps, "stopped": "quota", "errors": errors}
        except Exception as exc:  # noqa: BLE001 — um vídeo ruim não derruba o canal
            log.exception("falha no vídeo %s", v["video_id"])
            errors.append({"video_id": v["video_id"], "error": str(exc)})
    return {"videos": len(recent), "snapshots": snaps, "errors": errors}


# -- CLI --------------------------------------------------------------------
def _cli(argv=None):
    p = argparse.ArgumentParser(description="Coleta de métricas do YouTube")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("channel")
    sub.add_parser("videos")
    r = sub.add_parser("recent"); r.add_argument("--days", type=int, default=45)
    r.add_argument("--force", action="store_true")
    vv = sub.add_parser("video"); vv.add_argument("video_id")
    m = sub.add_parser("metrics"); m.add_argument("video_id")
    m.add_argument("--start"); m.add_argument("--end"); m.add_argument("--window")
    m.add_argument("--force", action="store_true")
    s = sub.add_parser("snapshot"); s.add_argument("video_id", nargs="?")
    s.add_argument("--all", action="store_true"); s.add_argument("--force", action="store_true")
    lk = sub.add_parser("link"); lk.add_argument("--apply", action="store_true")
    args = p.parse_args(argv)

    conn = storage.connect(); storage.init_db(conn)
    if args.cmd == "init":
        print("schema pronto:", cfg.DB_PATH); return
    if args.cmd == "link":
        from youtube import links
        for row in links.auto_link(conn, dry_run=not args.apply):
            print(f"  {row['short_key']:45s} -> {row.get('video_id') or '—'}  "
                  f"{row.get('matched_by', ''):9s} {row.get('confidence', 0)}")
        return

    try:
        if args.cmd in ("channel", "videos"):
            out = collect_channel(conn)
            print(f"canal {out['channel']['title']}: {out['saved']} vídeos")
            if args.cmd == "videos":
                for v in storage.all_videos(conn):
                    print(f"  {v['video_id']}  short={v['is_short']}  {v['title'][:70]}")
        elif args.cmd == "recent":
            print(collect_all_recent_videos(conn, days=args.days, force=args.force))
        elif args.cmd == "video":
            print(collect_video(args.video_id, conn))
        elif args.cmd == "metrics":
            snap = collect_metrics_for_video(
                args.video_id, args.start, args.end,
                age_window=args.window, force=args.force, conn=conn)
            print(snap or "nada gravado (já existia)")
        elif args.cmd == "snapshot":
            vids = storage.all_videos(conn) if args.all else [storage.get_video(conn, args.video_id)]
            total = 0
            for v in filter(None, vids):
                total += len(snapshot_due_windows(v, conn, force=args.force))
            print(f"{total} snapshot(s) criados")
    except AuthError as exc:
        print("ERRO de autenticação:", exc, file=sys.stderr); sys.exit(2)
    except QuotaError as exc:
        print("ERRO de quota:", exc, file=sys.stderr); sys.exit(3)


if __name__ == "__main__":
    _cli()
