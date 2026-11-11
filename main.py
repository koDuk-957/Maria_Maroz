import logging
import os
from pathlib import Path

from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


async def landing_page(_: web.Request) -> web.FileResponse:
    return web.FileResponse(BASE_DIR / "index.html")


async def old_miniapp_link(_: web.Request) -> web.HTTPFound:
    # Keep old shared links working, but use one canonical business-card URL.
    raise web.HTTPFound("/")


async def health(_: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", landing_page)
    app.router.add_get("/miniapp", old_miniapp_link)
    app.router.add_get("/health", health)
    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    web.run_app(create_app(), host="0.0.0.0", port=port)
