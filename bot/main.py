import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import start, check

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(check.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())