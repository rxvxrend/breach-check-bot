import requests

from services.checkers.base import BaseChecker


class UsernameChecker(BaseChecker):

    BASE_URL = "https://leakcheck.io/api/public"

    def fetch_data(self, username):

        try:
            responce = requests.get(
                self.BASE_URL,
                params={
                    "check": username
                },
                timeout=10
            )

            return responce
        
        except requests.RequestException:
            return {
                "success": False,
                "message": "Ошибка запроса к API"
            }

    def check(self, username):

        responce = self.fetch_data(username)

        if responce is None:
            return {
                "success": False,
                "message": "Ошибка соединения"
            }
        
        # ошибка api
        if responce.status_code != 200:
            return {
                "success": False,
                "message": f"API error: {responce.status_code}"
            }
        
        data = responce.json()

        # нет утечек (не ошибка)
        if data.get("success") is False:
            if data.get("error") == "Not found":
                return {
                    "success": True,
                    "found": False,
                    "count": 0,
                    "risk": "safe",
                    "sources": [],
                    "fields": []
                }
            
            # другие ошибки
            return {
                "success": False,
                "message": data.get("error", "Unkwown API error")
            }
        
        # есть утечки
        found = data.get("found", 0)
        fields = data.get("fields", [])
        sources = data.get("sources", [])
        
        return {
            "success": True,
            "found": found > 0,
            "count": found,
            "risk": self.calculate_risk(found, fields, sources),
            "sources": data.get("sources", []),
            "fields": data.get("fields", [])
        }
    
    def calculate_risk(self, count, fields, sources):

        score = 0
        reasons = []

        if count >= 50:
            score += 5
        elif count >= 10:
            score += 3
        elif count > 0:
            score += 1

        if "password" in fields:
            score += 5
            reasons.append("обнаружены пароли")
        if "phone" in fields:
            score += 2
            reasons.append("найдены номера телефонов")
        if "dob" in fields:
            score +=3
            reasons.append("найдена дата рождения")

        for source in sources:
            date = source.get("date", "")
            if date.startswith("2025") or date.startswith("2026"):
                score += 3
                reasons.append("обнаружены свежие утечки")
                break
        
        if score >= 10:
            return {
                "level": "critical",
                "reasons": reasons
            }
        if score >= 7:
            return {
                "level": "high",
                "reasons": reasons
            }
        if score >= 4:
            return {
                "level": "medium",
                "reasons": reasons
            }
        return {
                "level": "low",
                "reasons": reasons
            }