from typing import Optional
from .page import Page

class PageSet(list[Page]):
    def parse_item_group_for_all(
        self,
        query: str,
        model: dict,
        limit: Optional[int] = None
    ) -> list[dict]:
        dataset = []

        for page in self:
            adjusted_limit = limit if limit is None else limit - len(dataset)
            dataset.extend(page.parse_item_group(query, model, adjusted_limit))

        return dataset

    def parse_all(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> list[str]:
        dataset = []

        for page in self:
            if limit is not None and len(dataset) >= limit:
                break

            adjusted_limit = limit if limit is None else limit - len(dataset)
            dataset.extend(page.parse_all(query, adjusted_limit))

        return dataset