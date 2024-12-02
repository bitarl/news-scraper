import requests
from datetime import datetime

class PolygonNewsScraper:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://api.polygon.io/v2/reference/news"

    def fetch_news(self):
        params = {
            "apiKey": self.config["api_key"],
            "query": self.config["search_term"],
            "published_utc.gte": self.config["date_from"],
            "published_utc.lte": self.config["date_to"],
            "limit": 100,
        }
        # Handle specific date
        if self.config.get('date'):
            params["published_utc.gte"] = params["published_utc.lte"] = self.config["date"]

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return data.get("results", [])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
