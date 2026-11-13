"""Inline keyboards for the regular Telegram bot chat."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from config import CONTACT_USERNAME, MINIAPP_URL
from services_data import SERVICE_BUTTONS

CARD_URL = "https://maria-maroz-card.onrender.com"
MAX_URL = "https://max.ru/u/f9LHodD0cOIjPI4i_gTcSL_cyTen1knHz2e9woaTcjSEcXmEfE9WLhDpj9g"


def _contact_buttons() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text="Telegram",
            url=f"https://t.me/{CONTACT_USERNAME}",
        ),
        InlineKeyboardButton(text="MAX", url=MAX_URL),
    ]


def _brand_links() -> list[InlineKeyboardButton]:
    buttons = [InlineKeyboardButton(text="Сайт Марии", url=CARD_URL)]
    # Preserve the current Mini App URL and entry point without changing its code.
    if MINIAPP_URL:
        buttons.append(
            InlineKeyboardButton(
                text="Мини-приложение",
                web_app=WebAppInfo(url=MINIAPP_URL),
            )
        )
    return buttons


def main_menu_kb() -> InlineKeyboardMarkup:
    service_buttons = [
        InlineKeyboardButton(text=label, callback_data=f"service:{key}")
        for key, label in SERVICE_BUTTONS
    ]
    rows = [_brand_links()]
    rows.extend(
        service_buttons[index:index + 2]
        for index in range(0, len(service_buttons), 2)
    )
    rows.append(_contact_buttons())
    return InlineKeyboardMarkup(inline_keyboard=rows)


def service_kb(service_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            _contact_buttons(),
            [InlineKeyboardButton(text="← Все услуги", callback_data="menu")],
            _brand_links(),
        ]
    )


def contact_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[_contact_buttons()])
