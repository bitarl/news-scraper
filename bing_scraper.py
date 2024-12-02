import requests
from bs4 import BeautifulSoup


def get_article_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:

            return response.text
        else:
            print(f"Failed to fetch article content from '{url}'. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching article content from '{url}': {e}")
        return None


class BingScraper:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://www.bing.com"

    # Construct the complete URL by appending the search term to the base URL
    def fetch_news(self):
        url = f"{self.base_url}/news/search?q={self.config['search_term']}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Checks if request was successful
        except requests.RequestException as e:
            print(f"Failed to fetch news: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find news articles, adjusting the class as needed
        articles = soup.find_all("div", class_="t_s")[:200]

        news_data = []
        for article in articles:
            title_tag = article.find("a")
            if title_tag and "href" in title_tag.attrs:
                relative_url = title_tag["href"]
                full_url = f"{self.base_url}{relative_url}" if relative_url.startswith("/") else relative_url

                # Fetch and summarize the article content if the function exists
                article_text = get_article_text(full_url) if callable(get_article_text) else None

                news_data.append({
                    "title": title_tag.get_text(strip=True),
                    "url": full_url,
                    "summary": article_text
                })

        return news_data
