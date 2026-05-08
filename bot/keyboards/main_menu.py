from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text="🔑 Пароль")
    builder.button(text="📧 Email")
    builder.button(text="👤 Username")
    builder.button(text="🌐 Домен")

    builder.adjust(2)

    return builder.as_markup(
        resize_keyboard=True
    )