"""YouTube Data API v3 — descoberta e dados básicos dos vídeos do próprio canal.

Estratégia para evitar chamadas desnecessárias:
1. achar a playlist de uploads do canal (1 chamada, ``mine=true``);
2. listar os IDs por ela (``playlistItems.list``, 50 por página);
3. buscar detalhes em lote (``videos.list``, 50 IDs por chamada).

Custo de quota (unidades, não dinheiro): ``list`` ~1 unidade por chamada,
independente de quantos IDs no lote. Um canal com 300 vídeos custa ~6 chamadas
de ``playlistItems`` + ~6 de ``videos`` ≈ 12 unidades por coleta completa.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from youtube import config as cfg  # noqa: E402
from youtube.client import YouTubeClient  # noqa: E402
from youtube.errors import VideoUnavailableError, YouTubeError  # noqa: E402
from youtube.log import E_COLLECT_VIDEO, get_logger  # noqa: E402
from youtube.util import chunked, parse_iso8601_duration  # noqa: E402

log = get_logger("youtube.data")
SHORT_MAX_SECONDS = 180.0


def resolve_channel(client: YouTubeClient) -> dict:
    """{'channel_id', 'uploads_playlist_id', 'title'} do canal autenticado."""
    cid = cfg.credentials().get("channel_id")
    params = dict(part="contentDetails,snippet")
    if cid:
        params["id"] = cid
    else:
        params["mine"] = True
    resp = client.execute(client.data.channels().list(**params))
    items = resp.get("items") or []
    if not items:
        raise YouTubeError("Nenhum canal retornado (mine=true sem canal?).")
    ch = items[0]
    return {
        "channel_id": ch["id"],
        "uploads_playlist_id": ch["contentDetails"]["relatedPlaylists"]["uploads"],
        "title": ch.get("snippet", {}).get("title", ""),
    }


def list_channel_video_ids(client: YouTubeClient, uploads_playlist_id: str) -> list[dict]:
    """Todos os vídeos do canal: [{'video_id', 'published_at'}] via a playlist de uploads."""
    out, page = [], None
    while True:
        resp = client.execute(client.data.playlistItems().list(
            part="contentDetails", playlistId=uploads_playlist_id,
            maxResults=50, pageToken=page))
        for it in resp.get("items", []):
            cd = it.get("contentDetails", {})
            if cd.get("videoId"):
                out.append({"video_id": cd["videoId"],
                            "published_at": cd.get("videoPublishedAt")})
        page = resp.get("nextPageToken")
        if not page:
            return out


def get_videos(client: YouTubeClient, video_ids: list[str]) -> list[dict]:
    """Detalhes em lote. IDs ausentes na resposta (privados/removidos) são
    silenciosamente omitidos — quem chama compara com a lista pedida."""
    result = []
    for chunk in chunked(video_ids, 50):
        resp = client.execute(client.data.videos().list(
            part="snippet,contentDetails,statistics", id=",".join(chunk), maxResults=50))
        for v in resp.get("items", []):
            result.append(_video_dict(v))
    log.info("%s n=%d", E_COLLECT_VIDEO, len(result))
    return result


def get_video(client: YouTubeClient, video_id: str) -> dict:
    got = get_videos(client, [video_id])
    if not got:
        raise VideoUnavailableError(f"Vídeo {video_id} indisponível.")
    return got[0]


def _stat(stats: dict, key: str) -> int | None:
    v = stats.get(key)
    return int(v) if v is not None else None  # likeCount some vezes é ocultado


def _video_dict(v: dict) -> dict:
    sn, cd, st = v.get("snippet", {}), v.get("contentDetails", {}), v.get("statistics", {})
    dur = parse_iso8601_duration(cd.get("duration"))
    return {
        "video_id": v["id"],
        "title": sn.get("title", ""),
        "published_at": sn.get("publishedAt"),
        "channel_id": sn.get("channelId"),
        "duration_seconds": dur,
        "is_short": dur > 0 and dur <= SHORT_MAX_SECONDS,
        "view_count": _stat(st, "viewCount"),
        "like_count": _stat(st, "likeCount"),
        "comment_count": _stat(st, "commentCount"),
    }


if __name__ == "__main__":
    c = YouTubeClient()
    ch = resolve_channel(c)
    print("canal:", ch)
    ids = list_channel_video_ids(c, ch["uploads_playlist_id"])
    print(f"{len(ids)} vídeos no canal")
    for v in get_videos(c, [x["video_id"] for x in ids[:5]]):
        print(f"  {v['video_id']}  short={v['is_short']}  {v['duration_seconds']:.0f}s  {v['title'][:60]}")
