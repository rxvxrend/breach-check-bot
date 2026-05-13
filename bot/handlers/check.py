from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.check_states import CheckStates

from services.registry import get_checker
from services.storage import db
from services.formatters.breach_formatter import format_breach_result
from keyboards.monitoring_keyboards import get_monitoring_keyboard

router = Router()


@router.message(lambda message: message.text == "🔑 Пароль")
async def password_selected(message: Message, state: FSMContext):

    await state.update_data(check_type="password")

    await state.set_state(CheckStates.waiting_for_input)

    await message.answer(
        "🔑 Введите пароль для проверки:"
    )

@router.message(lambda message: message.text == "📧 Email")
async def email_selected(message: Message, state: FSMContext):

    await state.update_data(check_type="email")

    await state.set_state(CheckStates.waiting_for_input)

    await message.answer(
        "📧 Введите email для проверки:"
    )

@router.message(lambda message: message.text == "👤 Username")
async def email_selected(message: Message, state: FSMContext):

    await state.update_data(check_type="username")

    await state.set_state(CheckStates.waiting_for_input)

    await message.answer(
        "👤 Введите username для проверки:"
    )

@router.message(CheckStates.waiting_for_input)
async def process_input(message: Message, state: FSMContext):
    
    value = message.text

    data = await state.get_data()

    check_type = data.get("check_type")

    checker = get_checker(check_type)

    if not checker:
        await message.answer(
            "❌ Неизвестный тип проверки."
        )
        await state.clear()
        return
    
    result = checker.check(value)

    if not result["success"]:
        await message.answer(
            "❌ Ошибка при проверке."
        )
        await state.clear()
        return

    if result["found"]:
        responce = format_breach_result(result)
        
    else:
        responce = "✅ Не найдено в утечках."

    await message.answer(
        responce,
        reply_markup=get_monitoring_keyboard(
            db,
            message.from_user.id,
            check_type,
            value,
            result["count"]
        )
    )

    await state.clear()