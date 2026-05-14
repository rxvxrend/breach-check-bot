import hashlib
import aiohttp

from services.checkers.base import BaseChecker
from services.logger import logger
from services.http_client import http_client


class PasswordChecker(BaseChecker):

    API_URL = "https://api.pwnedpasswords.com/range/"

    def hash_password(self, password):
        return hashlib.sha1(
            password.encode()
        ).hexdigest().upper()
    
    async def get_pwned_data(self, prefix):
        try:
            responce = await http_client.get(
                f"{self.API_URL}{prefix}"
            )
                    
            if responce is None:
                return None

            if responce["status"] == 200:
                text = responce["text"]

                return dict(
                    line.split(":")
                    for line in text.splitlines()
                )
                    
            logger.error(
                f"HIBP bad status: {responce["status"]}"
            )
            return None
            
        except Exception as e:
            logger.error(f"HIBP request failed: {e}")
            return None
    
    async def check(self, password):
        hashed_password = self.hash_password(password)

        prefix = hashed_password[:5]
        suffix = hashed_password[5:]

        hashes = await self.get_pwned_data(prefix)

        if hashes is None:
            return {
                "success": False,
                "message": "Ошибка при запросе API."
            }
        
        count = int(hashes.get(suffix, 0))
        reasons = []

        if count > 100_000:
            risk_level = "critical"
            reasons.append("пароль чрезвычайно распространен в утечках")
        elif count > 500:
            risk_level = "high"
            reasons.append("пароль часто встречается в утечках")
        elif count > 0:
            risk_level = "medium"
            reasons.append("пароль был найден в утечках")
        else:
            risk_level = "safe"

        return {
            "success": True,
            "found": count > 0,
            "count": count,
            "risk": {
                "level": risk_level,
                "reasons": reasons
            }
        }