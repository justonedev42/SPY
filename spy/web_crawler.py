from httpx import AsyncClient
from parsel import Selector
from typing import Optional
import asyncio

class Crawler:
    def __init__(self, proxy: Optional[str] = None) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        }

        self.client = AsyncClient(
            headers = headers,
            http2 = True,
            proxy = proxy
        )

    async def fetch(self, url: str) -> Selector:
        response = await self.client.get(url)
        return Selector(text = response.text)
    
    async def get_all(self, urls: list[str]) -> list[Selector]:
        tasks = []

        for url in urls:
            tasks.append(self.fetch(url))

        pages = await asyncio.gather(*tasks)

        return pages