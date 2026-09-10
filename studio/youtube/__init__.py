"""Subsistema desacoplado de coleta de métricas do YouTube.

Autentica via OAuth 2.0 na conta do próprio canal, descobre os vídeos pela
playlist de uploads, coleta dados básicos (Data API v3) e de performance
(Analytics API), e persiste **snapshots históricos** em SQLite para estudar a
curva de crescimento dos Shorts e, depois, alimentar modelos de ranking.

Nada aqui usa LLM. Nada aqui faz scraping do YouTube Studio.
"""
