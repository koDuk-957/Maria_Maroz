"""Inline keyboards used by the Telegram bot."""
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

from config import CONTACT_USERNAME, MINIAPP_URL
from services_data import SERVICE_BUTTONS


def _contact_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Написать Марии",
        url=f"https://t.me/{CONTACT_USERNAME}",
    )


def main_menu_kb() -> InlineKeyboardMarkup:
    rows = []
    if MINIAPP_URL:
        rows.append([
            InlineKeyboardButton(
                text="Открыть визитку",
                web_app=WebAppInfo(url=MINIAPP_URL),
            )
        ])

    service_buttons = [
        InlineKeyboardButton(
            text=label,
            callback_data=f"service:{key}",
        )
        for key, label in SERVICE_BUTTONS
    ]
    rows.extend(
        [service_buttons[index:index + 2]
         for index in range(0, len(service_buttons), 2)]
    )
    rows.append([_contact_button()])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def service_kb(service_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [_contact_button()],
            [InlineKeyboardButton(text="« К услугам", callback_data="menu")],
        ]
    )


def contact_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[_contact_button()]])
