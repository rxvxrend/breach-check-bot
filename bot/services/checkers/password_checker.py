import hashlib
import requests

from services.checkers.base import BaseChecker


class PasswordChecker(BaseChecker):

    API_URL = "https://api.pwnedpasswords.com/range/"

    def hash_password(self, password):
        return hashlib.sha1(
            password.encode()
        ).hexdigest().upper()
    
    def get_pwned_data(self, prefix):
        try:
            responce = requests.get(
                f"{self.API_URL}{prefix}",
                timeout=5
            )

            if responce.status_code == 200:
                return dict(
                    line.split(":")
                    for line in responce.text.splitlines()
                )
            
        except requests.RequestException:
            return None
        
        return None
    
    def check(self, password):
        hashed_password = self.hash_password(password)

        prefix = hashed_password[:5]
        suffix = hashed_password[5:]

        hashes = self.get_pwned_data(prefix)

        if hashes is None:
            return {
                "success": False,
                "message": "Ошибка при запросе API."
            }
        
        count = int(hashes.get(suffix, 0))

        if count > 100_000:
            risk = "critical"
        elif count > 500:
            risk = "high"
        elif count > 0:
            risk = "medium"
        else:
            risk = "safe"

        return {
            "success": True,
            "found": count > 0,
            "count": count,
            "risk": risk
        }