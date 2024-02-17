from spy_crawler.web_crawler import Crawler
from spy_crawler.web_parser import Parser
import pandas as pd

class SPY:

    def __init__(self, proxy=None):
        self.crawler = Crawler(proxy)
        self.parser = Parser()
        self.pages = []

    async def paginate(self, url, links_selector, concat=False):
        page = await self.crawler.get_all([url])
        urls = page[0].css(links_selector).getall()

        if concat:
            urls = [url + path for path in urls]
        
        self.urls = urls

        return self

    async def get_all(self):
        self.pages = await self.crawler.get_all(self.urls)

    def get_items_group(self, group_selector, model):
        dataset = []
        for page in self.pages:
            dataset += self.parser.get_items_group(group_selector, model, page)

        return pd.DataFrame.from_records(dataset)
        