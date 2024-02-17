from .web_crawler import Crawler
from .web_parser import Parser
from typing import Self, Optional
import pandas as pd

class SPY:
    def __init__(self, proxy: Optional[str] = None) -> None:
        self.crawler = Crawler(proxy)
        self.parser = Parser()
        self.pages = []

    async def paginate(self, url: str, links_query: str, concat: bool = False) -> Self:
        page = await self.crawler.get_all([url])
        urls = page[0].css(links_query).getall()

        if concat:
            urls = [url + path for path in urls]
        
        self.urls = urls

        return self

    async def get_all(self) -> None:
        self.pages = await self.crawler.get_all(self.urls)

    def get_items_group(self, query: str, model: dict) -> pd.DataFrame:
        dataset = []
        
        for page in self.pages:
            dataset += self.parser.get_items_group(query, model, page)

        return pd.DataFrame.from_records(dataset)
        