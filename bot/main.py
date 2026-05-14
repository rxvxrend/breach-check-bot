import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import start, check, monitoring_handlers, subscriptions_handlers
from services.monitoring import monitoring_loop
from services.http_client import http_client

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(check.router)
    dp.include_router(monitoring_handlers.router)
    dp.include_router(subscriptions_handlers.router)

    await http_client.start()
    asyncio.create_task(monitoring_loop(bot))

    try:
        await dp.start_polling(bot)
    finally:
        await http_client.close()

if __name__ == "__main__":
    asyncio.run(main())