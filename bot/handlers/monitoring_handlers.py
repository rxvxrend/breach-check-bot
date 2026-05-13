from aiogram import Router
from aiogram.types import CallbackQuery

from services.storage import db

router = Router()

@router.callback_query()
async def monitoring_actions(callback: CallbackQuery):

    data = callback.data.split(":")
    action = data[0]

    if action == "unsub":
        _, check_type, value = data

        db.delete_subscription(
            user_id=callback.from_user.id,
            check_type=check_type,
            value=value
        )

        await callback.message.answer("❌ Удалено из мониторинга")
        await callback.answer("Удалено")

    elif action == "monitor":
        _, check_type, value, count = data

        db.add_subscription(
            user_id=callback.from_user.id,
            check_type=check_type,
            value=value,
            last_count=int(count)
        )
    
        await callback.message.answer(
            "✅ Добавлено в мониторинг"
        )
    
        await callback.answer()
