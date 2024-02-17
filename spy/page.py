from typing import Optional, Union
from parsel import Selector

class Page:
    def __init__(self, source: str) -> None:
        self.source = source

    def process_model(
        self,
        selector: Selector,
        model: Union[str, dict, list[dict]]
    ) -> Union[str, dict, list[dict]]:   
        data = {}

        for key in model:
            model_value = model[key]

            if isinstance(model_value, str):
                data[key] = selector.css(model_value).get()

            elif "field_type" in model_value:
                field_type = model_value["field_type"]

                if field_type == "multiple":
                    data[key] = selector.css(model_value["query"]).getall()

                    if "limit" in model_value and not model_value["limit"] is None:
                        data[key] = data[key][:model_value["limit"]]

                else:
                   data[key] = selector.css(model_value["query"]).get() 

            else:
                nested_model = model_value["model"]
                query = model_value["query"]
                is_group = model_value["is_group"] if "is_group" in model_value else False
                nested_selectors = selector.css(query)

                if is_group:
                    data[key] = [ self.process_model(nested_selector, nested_model) for nested_selector in nested_selectors ]
                
                else:
                    if len(nested_selectors) > 0:
                        nested_selector = nested_selectors[0]
                        data[key] = self.process_model(nested_selector, nested_model)

                    else:
                        data[key] = {}

        return data
            
    def parse_item_group(
        self,
        query: str,
        model: dict,
        limit: Optional[int] = None
    ) -> list[dict]:
        selector = Selector(self.source)
        parent_selectors = selector.css(query)

        dataset = []

        for child_selector in parent_selectors:
            if limit is not None and len(dataset) >= limit:
                break

            data = self.process_model(child_selector, model)
            dataset.append(data)

        return dataset

    def parse_item(self, query: str, model: dict) -> dict:
        data = self.parse_item_group(query, model, limit = 1)[0]
        return data

    def parse_all(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> list[str]:
        selector = Selector(self.source)

        selector_list = selector.css(query)
        dataset = selector_list.getall()

        if limit is not None and len(dataset) >= limit:
            dataset = dataset[:limit]

        return dataset

    def parse_one(self, query: str) -> str:
        data = self.parse_all(query, limit = 1)[0]
        return data