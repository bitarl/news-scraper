import requests
from datetime import datetime
# from newsapi import NewsApiClient

# Init
class NewsAPIScraper:
    def __init__(self, config):
        self.config = config
        self.newsapi = NewsApiClient(api_key=self.config["api_key"])

    def fetch_news(self):
        params = {
            "q": self.config['search_term'],
            "apiKey": self.config['api_key'],
            "sortBy": "publishedAt",
            "pageSize": 600,
            "language": "en",
            "domains": 'bbc.co.uk,techcrunch.com',
            "sources": 'bbc-news,the-verge',
            "from": self.config["date_from"],
            "to": self.config["date_to"],

        }
        # Handle date if specified
        if self.config.get('date'):
            params['from'] = params['to'] = self.config['date']

        articles = self.newsapi.get_everything(
           q=self.config['search_term'],
           from_param=self.config["date_from"],
           to=self.config["date_to"],
           language='en',
           sort_by='relevancy',
        )
        print(articles)
        return articles['articles'] if articles['status'] == 'ok' else []
