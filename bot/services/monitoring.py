import asyncio
from services.storage import db

from services.registry import CHECKERS


async def monitoring_loop(bot):
    
    while True:
        subscriptions = db.get_subscriptions()

        for subscription in subscriptions:
            try:

                (
                    sub_id,
                    user_id,
                    check_type,
                    value,
                    last_count
                ) = subscription

                checker = CHECKERS[check_type]
                
                result = checker.check(value)
                if not result["success"]:
                    continue

                new_count = result["count"]

                if new_count > last_count:

                    await bot.send_message(
                        user_id,
                        f"🚨 Новые утечки для {value}\n"
                        f"Было {last_count}\n"
                        f"Стало: {new_count}"
                    )

                    db.update_subscription(
                        sub_id,
                        new_count
                    )

            except Exception as e:
                print(f"Monitoring error: {e}")
        
        await asyncio.sleep(3600)