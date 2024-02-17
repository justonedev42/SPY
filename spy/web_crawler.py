from httpx import AsyncClient
from parsel import Selector
import asyncio


class Crawler:

    def __init__(self, proxy=None):
        headers={
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        }
        self.client = AsyncClient(headers=headers,http2=True, proxy=proxy)

    async def fetch(self, url):
        req = await self.client.get(url)
        return Selector(text=req.text)
    
    async def get_all(self, urls):
        tasks = []

        for url in urls:
            tasks.append(self.fetch(url))

        pages = await asyncio.gather(*tasks)
        return pages
