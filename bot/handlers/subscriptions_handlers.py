from aiogram import Router, F
from aiogram.types import Message

from services.storage import db
from keyboards.subscriptions_keyboards import get_subscriptions_keyboard

router = Router()

@router.message(F.text == "📂 Мои подписки")
async def show_subscriptions(message: Message):

    subscriptions = db.get_user_subscriptions(
        message.from_user.id
    )

    if not subscriptions:

        await message.answer(
            "📭 У вас нет подписок"
        )
        return
    
    responce = "📂 Ваши подписки:\n\n"

    for check_type, value, count in subscriptions:

        icons = {
            "email": "📧",
            "username": "👤",
            "password": "🔑"
        }
        responce += (
            f"{icons.get(check_type, '📌')}"
            f"{value}"
            f"({count} утечек)\n"
        )

    await message.answer(
        responce,
        reply_markup=get_subscriptions_keyboard(
            subscriptions
        )
    )