from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from keyboards import main_menu_kb, service_kb, contact_kb
from services_data import SERVICES

router = Router()

# Use the exact hero image URL from the business-card website.
WELCOME_PHOTO = (
    "https://images.pexels.com/photos/7534563/"
    "pexels-photo-7534563.jpeg?auto=compress&cs=tinysrgb&w=1400"
)

SERVICE_PHOTOS = {
    "consult": "https://images.pexels.com/photos/7641906/pexels-photo-7641906.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "ipoteka": "https://images.pexels.com/photos/16869705/pexels-photo-16869705.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "newbuild": "https://images.pexels.com/photos/30441428/pexels-photo-30441428.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "deals": "https://images.pexels.com/photos/6580378/pexels-photo-6580378.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "complex": "https://images.pexels.com/photos/8082227/pexels-photo-8082227.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "regions": "https://images.pexels.com/photos/7214456/pexels-photo-7214456.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "insurance": "https://images.pexels.com/photos/6797233/pexels-photo-6797233.jpeg?auto=compress&cs=tinysrgb&w=1000",
}


def format_service(service_key: str) -> str:
    data = SERVICES[service_key]
    lines = [
        f"✦  <b>{data['title']}</b>",
        "",
        f"<i>{data['subtitle']}</i>",
        "",
        "<b>В СОСТАВ УСЛУГИ</b>",
        "",
    ]
    for index, item in enumerate(data["items"], start=1):
        clean_item = item.replace("▪️ ", "").replace("• ", "")
        lines.append(f"<b>{index:02d}</b>  {clean_item}")
    lines.extend([
        "",
        "━━━━━━━━━━━━━━",
        f"<i>{data['footer']}</i>",
        "",
        "<b>Обсудим вашу задачу?</b>",
        "Напишите Марии — подскажем, с чего начать.",
    ])
    return "\n".join(lines)


async def replace_with_photo(message: Message, photo: str, caption: str, reply_markup) -> None:
    await message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML",
    )
    try:
        await message.delete()
    except Exception:
        pass


@router.message(CommandStart())
async def cmd_start(message: Message):
    # Telegram displays this caption directly under the photo, in one compact
    # message. Keep it deliberately short so the hero image remains dominant.
    caption = (
        "<b>МАРИЯ МАРОЗ</b>  <i>· эксперт по недвижимости</i>\n"
        "Помогаю выбрать недвижимость и пройти сделку спокойно и уверенно.\n"
        "<i>Выберите направление ниже</i>"
    )
    await message.answer_photo(
        photo=WELCOME_PHOTO,
        caption=caption,
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer_photo(
        photo=WELCOME_PHOTO,
        caption="<b>МАРИЯ МАРОЗ</b>\n<i>Выберите направление работы</i>",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


@router.message(Command("contact"))
async def cmd_contact(message: Message):
    await message.answer(
        "✦  <b>Связаться с Марией</b>\n\n"
        "Расскажите в двух словах о вашей задаче. "
        "Мария поможет определить дальнейшие шаги.",
        reply_markup=contact_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery):
    await replace_with_photo(
        callback.message,
        WELCOME_PHOTO,
        "<b>МАРИЯ МАРОЗ</b>\n<i>Выберите направление работы</i>",
        main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service:"))
async def callback_service(callback: CallbackQuery):
    service_key = callback.data.split(":", 1)[1]
    if service_key not in SERVICES:
        await callback.answer("Услуга не найдена", show_alert=True)
        return

    await replace_with_photo(
        callback.message,
        SERVICE_PHOTOS.get(service_key, WELCOME_PHOTO),
        format_service(service_key),
        service_kb(service_key),
    )
    await callback.answer()


@router.message()
async def any_message(message: Message):
    await message.answer(
        "Спасибо за сообщение. Выберите направление в меню "
        "или напишите Марии напрямую.",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )
