from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from keyboards import main_menu_kb, service_kb, contact_kb
from services_data import SERVICES, SERVICE_BUTTONS
from config import CONTACT_USERNAME

router = Router()


def format_service(service_key: str) -> str:
    data = SERVICES[service_key]
    lines = [
        f"<b>{data['title']}</b>",
        "",
        f"<i>{data['subtitle']}</i>",
        "",
    ]
    for item in data["items"]:
        lines.append(item)
    lines.append("")
    lines.append(f"▪️ <b>{data['footer']}</b>")
    return "\n".join(lines)


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "<b>Мария Мароз</b>\n"
        "Эксперт по недвижимости\n\n"
        "Помогаю с покупкой, продажей, ипотекой, "
        "сложными сделками, новостройками и доходной недвижимостью "
        "по всей России.\n\n"
        "Выберите интересующую услугу или сразу напишите мне в личные сообщения:"
    )
    await message.answer(text, reply_markup=main_menu_kb(), parse_mode="HTML")


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "Выберите услугу:",
        reply_markup=main_menu_kb(),
    )


@router.message(Command("contact"))
async def cmd_contact(message: Message):
    text = (
        f"Связаться с Марией Мароз:\n"
        f"👉 @{CONTACT_USERNAME}\n\n"
        "Напишите в личные сообщения — обсудим вашу задачу."
    )
    await message.answer(text, reply_markup=contact_kb())


@router.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите услугу:",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service:"))
async def callback_service(callback: CallbackQuery):
    service_key = callback.data.split(":")[1]
    if service_key not in SERVICES:
        await callback.answer("Услуга не найдена", show_alert=True)
        return

    text = format_service(service_key)
    await callback.message.edit_text(
        text,
        reply_markup=service_kb(service_key),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message()
async def any_message(message: Message):
    """Любое другое сообщение — предлагаем меню или контакт"""
    await message.answer(
        "Выберите услугу из меню или напишите мне напрямую:",
        reply_markup=main_menu_kb(),
    )
