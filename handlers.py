from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from keyboards import main_menu_kb, service_kb, contact_kb
from services_data import SERVICES
from config import CONTACT_USERNAME

router = Router()

# Editorial property image already used on Maria's separate business-card site.
WELCOME_PHOTO = (
    "https://images.pexels.com/photos/30441428/"
    "pexels-photo-30441428.jpeg?auto=compress&cs=tinysrgb&w=1400"
)


def format_service(service_key: str) -> str:
    data = SERVICES[service_key]
    lines = [
        f"✦  <b>{data['title']}</b>",
        "",
        f"<i>{data['subtitle']}</i>",
        "",
        "<tg-spoiler>Что входит в сопровождение</tg-spoiler>",
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
        "<b>Хотите обсудить вашу ситуацию?</b>",
        "Напишите Марии — подскажем, с чего лучше начать.",
    ])
    return "\n".join(lines)


async def edit_screen(message: Message, text: str, reply_markup) -> None:
    """Update either the welcome photo caption or a regular text message."""
    if message.photo:
        await message.edit_caption(
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    else:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "МАРИЯ МАРОЗ\n"
        "<i>Эксперт по недвижимости</i>\n"
        "━━━━━━━━━━━━━━\n\n"
        "Недвижимость — это не только квадратные метры. "
        "Это важное решение, в котором имеют значение детали, "
        "условия и уверенность на каждом этапе.\n\n"
        "Помогаю с покупкой и продажей, ипотекой, новостройками "
        "и нестандартными сделками по всей России.\n\n"
        "<b>Выберите направление, чтобы узнать подробнее.</b>"
    )
    await message.answer_photo(
        photo=WELCOME_PHOTO,
        caption=text,
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "✦  <b>Направления работы</b>\n\n"
        "Выберите интересующую услугу. Если пока не знаете, "
        "с чего начать, можно сразу написать Марии.",
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
    await edit_screen(callback.message, text, main_menu_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("service:"))
async def callback_service(callback: CallbackQuery):
    service_key = callback.data.split(":", 1)[1]
    if service_key not in SERVICES:
        await callback.answer("Услуга не найдена", show_alert=True)
        return

    await edit_screen(
        callback.message,
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
