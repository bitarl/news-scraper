import requests
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
    

class NewsAPIScraper(NewsScraper):
    def __init__(self, search_term, config):
        super().__init__(search_term, config)
        self.base_url = config.get('endpoint', 'https://newsapi.org/v2/everything')

    def fetch_news(self):
        params = {
            "q": self.search_term,
            "apiKey": self.config['endpoint_key'],
            "language": self.config.get('language', 'en'),
            "sortBy": "publishedAt"  # Default sorting by latest news
        }
        # Handle date or latest news option
        if 'date' in self.config:
            from_date, to_date = self.config['date'], self.config['date']
            params.update({"from": from_date, "to": to_date})
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return self._create_response(200, response.json()['articles'])
        else:
            return self._create_response(response.status_code, [])


class BingScraper(NewsScraper):
    def __init__(self, search_term, config):
        super().__init__(search_term, config)
        self.base_url = "https://www.bing.com/news/search"

    def fetch_news(self):
        params = {
            "q": self.search_term,
            "form": "HDRSC6"  # Assuming this is a form that might exist for structured searches
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all("div", class_="news-card newsitem cardcommon b_cards2")
            news_data = [{
                "title": article.find("a").text,
                "url": article.find("a")["href"]
            } for article in articles]
            return self._create_response(200, news_data)
        else:
            return self._create_response(response.status_code, [])


class RedditScraper(NewsScraper):
    def __init__(self, search_term, config):
        super().__init__(search_term, config)
        self.base_url = "https://www.reddit.com/search.json"

    def fetch_news(self):
        params = {
            "q": self.search_term,
            "limit": 10,
            "sort": "new"  # Default sorting by new
        }
        if 'time_filter' in self.config:  # Expecting values like 'day', 'week', 'month', 'year', 'all'
            params.update({"t": self.config['time_filter']})
        headers = {'User-agent': 'your bot 0.1'}
        response = requests.get(self.base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            news_data = [{
                "title": item['data']['title'],
                "url": item['data']['url'],
                "subreddit": item['data']['subreddit']
            } for item in data['data']['children']]
            return self._create_response(200, news_data)
        else:
            return self._create_response(response.status_code, [])


config_newsapi = {
    "endpoint_key": "your_newsapi_key",
    "language": "en",
    "date": "2023-05-05"
}

newsapi_scraper = NewsAPIScraper("climate change", config_newsapi)
print(newsapi_scraper.fetch_news())

reddit_config = {
    "time_filter": "day"
}

reddit_scraper = RedditScraper("technology", reddit_config)
print(reddit_scraper.fetch_news())

bing_scraper = BingScraper("latest news", {})
print(bing_scraper.fetch_news())
