from abc import ABC, abstractmethod


class NewsScraper(ABC):
    def __init__(self, search_term, config):
        self.search_term = search_term
        self.config = config

    @abstractmethod
    def fetch_news(self):
        pass

    def _create_response(self, status_code, data):
        return {
            "status_code": status_code,
            "data": data
        }
    