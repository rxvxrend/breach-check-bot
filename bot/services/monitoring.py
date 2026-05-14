import asyncio
from services.storage import db

from services.registry import CHECKERS
from services.logger import logger


async def monitoring_loop(bot):

    logger.info("Monitoring loop started")
    while True:
        
        subscriptions = db.get_subscriptions()
        logger.info(
            f"Checking {len(subscriptions)} subscriptions"
        )

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
                
                logger.info(
                    f"Checking {check_type}: {value}"
                )

                result = await checker.check(value)
                if not result["success"]:
                    continue

                new_count = result["count"]

                if new_count > last_count:

                    logger.warning(
                        f"New breaches found for {value}: "
                        f"{last_count} -> {new_count}"
                    )

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
                logger.exception(
                    f"Monitoring error for {value}: {e}"
                )
        
        await asyncio.sleep(3600)