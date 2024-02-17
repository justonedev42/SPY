from httpx import AsyncClient
from typing import Optional
from .page_set import PageSet
from .page import Page
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

    async def fetch(self, url: str) -> Page:
        response = await self.client.get(url)
        return Page(response.text)
    
    async def get_all(self, urls: list[str]) -> PageSet[Page]:
        tasks = []

        for url in urls:
            tasks.append(self.fetch(url))

        pages = PageSet(await asyncio.gather(*tasks))

        return pages