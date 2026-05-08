from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.main_menu import get_main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Выберите тип проверки:",
        reply_markup=get_main_menu()
    )