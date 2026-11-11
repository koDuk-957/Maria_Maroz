"""
Простой Telegram-бот визитка Марии Мароз
- /start — приветствие + кнопка открыть мини-приложение + кнопка написать
- Меню услуг (кратко)
- Кнопка перехода в личку @Maroz_Maria
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CONTACT_USERNAME = os.getenv("CONTACT_USERNAME", "Maroz_Maria")

# URL вашего мини-приложения (после хостинга замените на реальный HTTPS)
# Примеры: GitHub Pages, Netlify, Vercel, Timeweb и т.д.
MINIAPP_URL = os.getenv("MINIAPP_URL", "https://your-domain.com/miniapp.html")

if not BOT_TOKEN:
    raise ValueError("Укажите BOT_TOKEN в файле .env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()


def main_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="📋 Открыть визитку",
                web_app=WebAppInfo(url=MINIAPP_URL),
            )
        ],
        [
            InlineKeyboardButton(
                text="✍️ Написать Марии",
                url=f"https://t.me/{CONTACT_USERNAME}",
            )
        ],
        [
            InlineKeyboardButton(text="Ипотека", callback_data="s:ipoteka"),
            InlineKeyboardButton(text="Новостройки", callback_data="s:newbuild"),
        ],
        [
            InlineKeyboardButton(text="Сделки", callback_data="s:deals"),
            InlineKeyboardButton(text="Сложные сделки", callback_data="s:complex"),
        ],
        [
            InlineKeyboardButton(text="Консультация", callback_data="s:consult"),
            InlineKeyboardButton(text="Все услуги", callback_data="s:all"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✍️ Написать Марии",
                    url=f"https://t.me/{CONTACT_USERNAME}",
                )
            ],
            [InlineKeyboardButton(text="« Назад", callback_data="menu")],
        ]
    )


TEXTS = {
    "consult": (
        "<b>Бесплатная консультация</b>\n\n"
        "• Разбор вашего запроса\n"
        "• Предварительная оценка ситуации\n"
        "• Обсуждение вариантов решения\n"
        "• Условия и этапы дальнейшей работы\n\n"
        "Первый шаг к решению вопроса с недвижимостью."
    ),
    "ipoteka": (
        "<b>Ипотека</b>\n\n"
        "Семейная, военная, IT-ипотека и другие программы.\n\n"
        "• Подбор программы и банка\n"
        "• Работа со сложной кредитной историей\n"
        "• Анализ причин отказов\n"
        "• Подготовка заявки и сопровождение одобрения"
    ),
    "newbuild": (
        "<b>Новостройки</b> — услуги для покупателя <b>0 ₽</b>\n\n"
        "• Сравнение условий застройщиков\n"
        "• Экспертная оценка ЖК\n"
        "• Выбор квартиры под бюджет\n"
        "• Акции, спецпредложения и закрытые лоты\n"
        "• Сопровождение до получения ключей\n\n"
        "Покупка по спеццене + моё сопровождение в подарок."
    ),
    "deals": (
        "<b>Сделки с недвижимостью</b>\n\n"
        "Покупка и продажа: квартиры, дома, участки.\n\n"
        "• Анализ рыночной стоимости\n"
        "• Подбор объектов и переговоры\n"
        "• Проверка документов и рисков\n"
        "• Полное сопровождение до ключей\n\n"
        "360+ сделок. Рекорд — 14 дней."
    ),
    "complex": (
        "<b>Сложные сделки</b>\n\n"
        "Наследство, доли, несколько собственников, иностранные граждане.\n\n"
        "• Анализ документов и обстоятельств\n"
        "• Поиск законного решения\n"
        "• Согласование интересов\n"
        "• Организация сделки со специалистами"
    ),
    "all": (
        "<b>Все услуги Марии Мароз</b>\n\n"
        "1. Бесплатная консультация\n"
        "2. Ипотека\n"
        "3. Новостройки (0 ₽ для покупателя)\n"
        "4. Сделки на вторичном рынке\n"
        "5. Сложные сделки\n"
        "6. Недвижимость по всей России\n"
        "7. Посуточная аренда и управление\n"
        "8. Доходная недвижимость\n"
        "9. Страхование недвижимости\n\n"
        "Откройте визитку или напишите в личку — разберём вашу задачу."
    ),
}


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "<b>Мария Мароз</b>\n"
        "Эксперт по недвижимости\n\n"
        "Ипотека · Новостройки · Сложные сделки · Доходная недвижимость\n\n"
        "Откройте визитку или сразу напишите мне:"
    )
    await message.answer(text, reply_markup=main_kb())


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Выберите действие:", reply_markup=main_kb())


@router.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=main_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("s:"))
async def cb_service(callback: CallbackQuery):
    key = callback.data.split(":")[1]
    text = TEXTS.get(key, "Услуга не найдена")
    await callback.message.edit_text(text, reply_markup=back_kb())
    await callback.answer()


@router.message()
async def any_msg(message: Message):
    await message.answer(
        "Нажмите кнопку ниже или напишите /start",
        reply_markup=main_kb(),
    )


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)
    logger.info("Простой бот Марии Мароз запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
