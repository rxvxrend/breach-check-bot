import aiohttp
import asyncio
from services.logger import logger

class HttpClient:
    def __init__(self):
        self.session: aiohttp.ClientSession | None = None

    async def start(self):
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=10)

            self.session = aiohttp.ClientSession(timeout=timeout)

            logger.info("HTTP client started")

    async def get(self, url, params=None, retries=3):
        if not self.session:
            await self.start()

        last_error = None

        for attempt in range(1, retries + 1):
            try:
                async with self.session.get(url, params=params) as responce:
                    text = await responce.text()

                    return {
                        "status": responce.status,
                        "text": text
                    }
            
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_error = e
                logger.warning(
                    f"HTTP retry {attempt}/{retries} failed: {e}"
                )

                if attempt < retries:
                    await asyncio.sleep(2 ** (attempt - 1)) # backoff 1s -> 2s -> 4s
                
        logger.error(f"HTTP failed after {retries} retries: {last_error}")
        return None
        
    async def get_json(self, url, params=None):
        async with self.session.get(url, params=params) as repsonce:
            return {
                "status": repsonce.status,
                "data": await repsonce.json()
            }
        
    async def close(self):
        if self.session:
            await self.session.close()
            logger.info("HTTP client closed")

http_client = HttpClient()