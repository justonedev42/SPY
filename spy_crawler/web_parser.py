class Parser:
    def __init__(self):
        pass

    def get_items_group(self, group_selector, model, page):
        data = page.css(group_selector)
        dataset = []
        for e in data:
            dataset.append({ k: e.css(v).get() for k,v in model.items() })

        return dataset