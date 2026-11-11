import logging
import os
import secrets
import hmac

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update

from config import BOT_TOKEN
from handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

WEBHOOK_PATH = "/telegram-webhook"


def create_app() -> web.Application:
    if not BOT_TOKEN:
        raise RuntimeError(
            "Не задан BOT_TOKEN. Добавьте токен Telegram-бота в переменные окружения."
        )

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)
    webhook_secret = secrets.token_urlsafe(32)

    async def health(_: web.Request) -> web.Response:
        return web.json_response({"status": "ok"})

    async def telegram_webhook(request: web.Request) -> web.Response:
        supplied_secret = request.headers.get(
            "X-Telegram-Bot-Api-Secret-Token", ""
        )
        if not hmac.compare_digest(supplied_secret, webhook_secret):
            raise web.HTTPUnauthorized(text="Invalid webhook secret")

        try:
            payload = await request.json()
            update = Update.model_validate(payload, context={"bot": bot})
            await dp.feed_update(bot, update)
        except (ValueError, TypeError):
            logger.exception("Не удалось обработать обновление Telegram")
            raise web.HTTPBadRequest(text="Invalid update")

        return web.Response(text="ok")

    async def on_startup(_: web.Application) -> None:
        base_url = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
        if not base_url:
            raise RuntimeError(
                "Не найдена переменная RENDER_EXTERNAL_URL. "
                "Запускайте приложение как Render Web Service."
            )

        await bot.set_webhook(
            url=f"{base_url}{WEBHOOK_PATH}",
            secret_token=webhook_secret,
            drop_pending_updates=False,
        )
        logger.info("Webhook установлен: %s%s", base_url, WEBHOOK_PATH)

    async def on_cleanup(_: web.Application) -> None:
        await bot.session.close()

    app = web.Application()
    app.router.add_get("/health", health)
    app.router.add_post(WEBHOOK_PATH, telegram_webhook)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    web.run_app(create_app(), host="0.0.0.0", port=port)
