from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_monitoring_keyboard(db, user_id, check_type, value, count):

    builder = InlineKeyboardBuilder()

    is_subscribed = db.is_subscribed(user_id, check_type, value)
    
    if is_subscribed:
        builder.button(
            text="❌ Удалить из мониторинга",
            callback_data=f"unsub:{check_type}:{value}"
        )

    else:
        builder.button(
            text="📌 Добавить в мониторинг",
            callback_data=f"monitor:{check_type}:{value}:{count}"
        )

    return builder.as_markup()