import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "Не задан BOT_TOKEN. Добавьте токен Telegram-бота в переменные окружения."
        )

    async with Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    ) as bot:
        dp = Dispatcher()
        dp.include_router(router)

        # Polling cannot run while a webhook is active.
        await bot.delete_webhook(drop_pending_updates=False)
        logger.info("Бот Марии Мароз запущен")
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
