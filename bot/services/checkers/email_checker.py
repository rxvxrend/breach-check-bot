import requests

from services.checkers.base import BaseChecker


class EmailChecker(BaseChecker):

    BASE_URL = "https://leakcheck.io/api/public"

    def fetch_data(self, email):

        try:
            responce = requests.get(
                self.BASE_URL,
                params={
                    "check": email
                },
                timeout=5
            )

            return responce
        
        except requests.RequestException:
            return None

    def check(self, email):

        responce = self.fetch_data(email)

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
        
        return {
            "success": True,
            "found": found > 0,
            "count": found,
            "risk": self.calculate_risk(found),
            "sources": data.get("sources", []),
            "fields": data.get("fields", [])
        }
    
    def calculate_risk(self, breach_count):

        if breach_count >= 10:
            return "critical"
        
        if breach_count >= 5:
            return "high"
        
        if breach_count > 0:
            return "medium"
        
        return "safe"