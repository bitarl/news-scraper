import requests

class RedditScraper:
    def __init__(self, config):
        self.config = config

    def fetch_news(self):
        headers = {'User-agent': 'your bot 0.1'}
        url = f"https://www.reddit.com/search.json?q={self.config['search_term']}&sort=new&limit=700"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return [{"title": item['data']['title'], "url": item['data']['url']} for item in data['data']['children']]
        return []
