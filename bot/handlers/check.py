from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.check_states import CheckStates

from services.checkers.password_checker import PasswordChecker

router = Router()

password_checker = PasswordChecker()

@router.message(lambda message: message.text == "🔑 Пароль")
async def password_selected(message: Message, state: FSMContext):
    await state.set_state(CheckStates.waiting_for_password)

    await message.answer(
        "🔑 Введите пароль для проверки:"
    )

@router.message(CheckStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text

    result = password_checker.check(password)

    if not result["success"]:
        await message.answer(
            "❌ Ошибка при проверке."
        )
        return

    if result["found"]:
        responce = (
            f"⚠️ Пароль найден в утечках!\n"
            f"Количество: {result['count']}\n"
            f"Риск: {result['risk']}"
        )
    else:
        responce = "✅ Пароль не найден в утечках."

    await message.answer(responce)

    await state.clear()