from parsel import Selector

class Parser:
    def __init__(self):
        pass

    def get_items_group(self, query: str, model: dict, page: Selector) -> list[dict]:
        data = page.css(query)
        dataset = []

        for e in data:
            dataset.append({ k: e.css(v).get() for k,v in model.items() })

        return dataset