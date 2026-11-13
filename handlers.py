from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from keyboards import main_menu_kb, service_kb, contact_kb
from services_data import SERVICES

router = Router()

# The exact hero photograph used on Maria's business-card website.
WELCOME_PHOTO = (
    "https://images.pexels.com/photos/7534563/"
    "pexels-photo-7534563.jpeg?auto=compress&cs=tinysrgb&w=1400"
)

# These are the same photographs used in the corresponding service cards
# on the business-card website.
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
    """Send the next branded screen, then remove the previous bot menu message."""
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
    text = (
        "<b>МАРИЯ МАРОЗ</b>\n"
        "<i>Эксперт по недвижимости</i>\n"
        "━━━━━━━━━━━━━━\n"
        "Помогаю выбрать недвижимость и безопасно пройти путь "
        "от первого вопроса до сделки.\n\n"
        "<b>Выберите направление — расскажу подробнее.</b>"
    )
    await message.answer_photo(
        photo=WELCOME_PHOTO,
        caption=text,
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    text = (
        "✦  <b>Направления работы</b>\n\n"
        "Выберите услугу или свяжитесь с Марией напрямую."
    )
    await message.answer_photo(
        photo=WELCOME_PHOTO,
        caption=text,
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


@router.message(Command("contact"))
async def cmd_contact(message: Message):
    text = (
        "✦  <b>Связаться с Марией</b>\n\n"
        "Расскажите в двух словах о вашей задаче. "
        "Мария поможет определить дальнейшие шаги."
    )
    await message.answer(
        text,
        reply_markup=contact_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery):
    text = (
        "✦  <b>Направления работы</b>\n\n"
        "Выберите интересующую услугу. "
        "Можно также написать Марии напрямую."
    )
    await replace_with_photo(
        callback.message,
        WELCOME_PHOTO,
        text,
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
        "Спасибо за сообщение. Чтобы быстрее сориентироваться, "
        "выберите направление в меню или напишите Марии напрямую.",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )
