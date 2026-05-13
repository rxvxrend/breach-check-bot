from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_subscriptions_keyboard(subscriptions):

    builder = InlineKeyboardBuilder()

    for check_type, value, count in subscriptions:
        
        builder.button(
            text=f"❌ {value}",
            callback_data=f"unsub:{check_type}:{value}"
        )
        builder.adjust(1)

    return builder.as_markup()