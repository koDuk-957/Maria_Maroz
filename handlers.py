from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram.exceptions import TelegramAPIError

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
    "consult": "https://images.pexels.com/photos/5997965/pexels-photo-5997965.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "ipoteka": "https://images.pexels.com/photos/7167077/pexels-photo-7167077.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "newbuild": "https://images.pexels.com/photos/18822072/pexels-photo-18822072.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "deals": "https://images.pexels.com/photos/14921656/pexels-photo-14921656.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "complex": "https://images.pexels.com/photos/10610731/pexels-photo-10610731.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "regions": "https://images.pexels.com/photos/5033768/pexels-photo-5033768.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "insurance": "https://images.pexels.com/photos/6587864/pexels-photo-6587864.jpeg?auto=compress&cs=tinysrgb&w=1200",
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


WELCOME_CAPTION = (
    "<b>МАРИЯ МАРОЗ</b>\n"
    "<i>Эксперт по недвижимости</i>\n"
    "Подбор недвижимости и сопровождение сделок по всей России.\n"
    "<i>Выберите направление ниже.</i>"
)


async def show_menu_in_place(
    message: Message,
    photo: str,
    caption: str,
    reply_markup,
) -> None:
    """Edit the existing menu card; only send a replacement if editing fails."""
    try:
        await message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption,
                parse_mode="HTML",
            ),
            reply_markup=reply_markup,
        )
        return
    except TelegramAPIError:
        # Some older menu messages may be text-only or otherwise not editable
        # as media. Send the replacement first, then remove only that old
        # bot-generated menu message. Never delete a user's message here.
        replacement = await message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
        try:
            await message.delete()
        except TelegramAPIError:
            # If Telegram refuses deletion, keep the new working menu rather
            # than risk losing navigation.
            pass


@router.message(CommandStart())
async def cmd_start(message: Message):
    # A fresh /start intentionally creates a new entry point. The command
    # itself and all user messages are preserved.
    await message.answer_photo(
        photo=WELCOME_PHOTO,
        caption=WELCOME_CAPTION,
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
    await show_menu_in_place(
        callback.message,
        WELCOME_PHOTO,
        WELCOME_CAPTION,
        main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service:"))
async def callback_service(callback: CallbackQuery):
    service_key = callback.data.split(":", 1)[1]
    if service_key not in SERVICES:
        await callback.answer("Услуга не найдена", show_alert=True)
        return

    await show_menu_in_place(
        callback.message,
        SERVICE_PHOTOS.get(service_key, WELCOME_PHOTO),
        format_service(service_key),
        service_kb(service_key),
    )
    await callback.answer()


# Intentionally no catch-all message handler: ordinary user messages stay
# in the conversation without the bot replying with another full menu.
