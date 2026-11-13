"""Inline keyboards for the regular Telegram bot chat."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from config import CONTACT_USERNAME, MINIAPP_URL
from services_data import SERVICE_BUTTONS

CARD_URL = "https://maria-maroz-card.onrender.com"
MAX_URL = "https://max.ru/u/f9LHodD0cOIjPI4i_gTcSL_cyTen1knHz2e9woaTcjSEcXmEfE9WLhDpj9g"


def _contact_buttons() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text="Написать в Telegram",
            url=f"https://t.me/{CONTACT_USERNAME}",
        ),
        InlineKeyboardButton(text="Написать в MAX", url=MAX_URL),
    ]


def main_menu_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="Сайт-визитка", url=CARD_URL)],
    ]

    # Keep the existing Mini App entry point intact.
    if MINIAPP_URL:
        rows.append([
            InlineKeyboardButton(
                text="Открыть мини-приложение",
                web_app=WebAppInfo(url=MINIAPP_URL),
            )
        ])

    service_buttons = [
        InlineKeyboardButton(text=label, callback_data=f"service:{key}")
        for key, label in SERVICE_BUTTONS
    ]
    rows.extend(
        [service_buttons[index:index + 2]
         for index in range(0, len(service_buttons), 2)]
    )
    rows.append(_contact_buttons())
    return InlineKeyboardMarkup(inline_keyboard=rows)


def service_kb(service_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            _contact_buttons(),
            [InlineKeyboardButton(text="← Все услуги", callback_data="menu")],
            [InlineKeyboardButton(text="Сайт-визитка", url=CARD_URL)],
        ]
    )


def contact_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[_contact_buttons()])
