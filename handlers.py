from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from keyboards import main_menu_kb, service_kb, contact_kb
from services_data import SERVICES

router = Router()

# Separate photo set for the regular bot. These images intentionally do not
# repeat the photographs inside the Mini App / electronic business card.
WELCOME_PHOTO = (
    "https://images.pexels.com/photos/7599735/"
    "pexels-photo-7599735.jpeg?auto=compress&cs=tinysrgb&w=1200"
)

SERVICE_PHOTOS = {
    "consult": "https://images.pexels.com/photos/7642008/pexels-photo-7642008.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "ipoteka": "https://images.pexels.com/photos/31221014/pexels-photo-31221014.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "newbuild": "https://images.pexels.com/photos/31015267/pexels-photo-31015267.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "deals": "https://images.pexels.com/photos/29726512/pexels-photo-29726512.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "complex": "https://images.pexels.com/photos/34135038/pexels-photo-34135038.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "regions": "https://images.pexels.com/photos/16869705/pexels-photo-16869705.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "insurance": "https://images.pexels.com/photos/7736033/pexels-photo-7736033.jpeg?auto=compress&cs=tinysrgb&w=1200",
}

SERVICE_SHORT_TEXT = {
    "consult": "Разберём задачу, бюджет и подходящие варианты.",
    "ipoteka": "Подбор программы и сопровождение до одобрения.",
    "newbuild": "Подбор новостройки, проверка условий и сопровождение до ключей.",
    "deals": "Покупка и продажа квартир, домов и участков.",
    "complex": "Наследство, доли и сделки с несколькими собственниками.",
    "regions": "Подбор недвижимости в Москве, Санкт-Петербурге и на юге России.",
    "insurance": "Защита недвижимости, отделки и имущества.",
}


def format_service(service_key: str) -> str:
    data = SERVICES[service_key]
    short_text = SERVICE_SHORT_TEXT.get(service_key, data["subtitle"])
    return (
        f"<b>✦  {data['title']}</b>\n"
        f"<i>{short_text}</i>\n\n"
        "Подробности и все условия — в мини-приложении.\n"
        "<b>Обсудим вашу задачу?</b>"
    )


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
    caption = (
        "<b>МАРИЯ МАРОЗ</b>\n"
        "<i>Эксперт по недвижимости</i>\n"
        "Помогаю выбрать объект и спокойно пройти путь до сделки.\n"
        "<i>Выберите направление ниже.</i>"
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
        caption="<b>МАРИЯ МАРОЗ</b>\n<i>Выберите направление работы.</i>",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


@router.message(Command("contact"))
async def cmd_contact(message: Message):
    await message.answer(
        "<b>Связаться с Марией</b>\n"
        "Напишите удобным способом — обсудим вашу задачу.",
        reply_markup=contact_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu")
async def callback_menu(callback: CallbackQuery):
    await replace_with_photo(
        callback.message,
        WELCOME_PHOTO,
        "<b>МАРИЯ МАРОЗ</b>\n<i>Выберите направление работы.</i>",
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
        "Выберите направление в меню или напишите Марии напрямую.",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )
