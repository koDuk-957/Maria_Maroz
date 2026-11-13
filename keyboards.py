"""Inline keyboards for the regular Telegram bot chat."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from config import CONTACT_USERNAME, MINIAPP_URL
from services_data import SERVICE_BUTTONS

MAX_URL = "https://max.ru/u/f9LHodD0cOIjPI4i_gTcSL_cyTen1knHz2e9woaTcjSEcXmEfE9WLhDpj9g"
APP_URL = MINIAPP_URL or "https://maria-maroz.onrender.com/miniapp"


def _contact_buttons() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(text="Написать в Telegram", url=f"https://t.me/{CONTACT_USERNAME}"),
        InlineKeyboardButton(text="Написать в MAX", url=MAX_URL),
    ]


def _miniapp_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Портфолио и услуги",
        web_app=WebAppInfo(url=APP_URL),
    )


def main_menu_kb() -> InlineKeyboardMarkup:
    service_buttons = [
        InlineKeyboardButton(text=label, callback_data=f"service:{key}")
        for key, label in SERVICE_BUTTONS
    ]
    rows = [[_miniapp_button()]]
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
            [InlineKeyboardButton(text="Все направления", callback_data="menu")],
            [_miniapp_button()],
        ]
    )


def contact_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[_contact_buttons()])
