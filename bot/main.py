import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import start, check, monitoring_handlers, subscriptions_handlers
from services.monitoring import monitoring_loop

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(check.router)
    dp.include_router(monitoring_handlers.router)
    dp.include_router(subscriptions_handlers.router)

    asyncio.create_task(
        monitoring_loop(bot)
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())