from news_scrapers.newsapi_scraper import NewsAPIScraper
from news_scrapers.bing_scraper import BingScraper
from news_scrapers.reddit_scraper import RedditScraper

from preprocessing.data_preprocessor import DataPreprocessor

from executor.pipeline_executor import NewsPipelineExecutor

import os
from datetime import datetime

from news_scrapers.newsapi_scraper import NewsAPIScraper
from news_scrapers.bing_scraper import BingScraper
from news_scrapers.reddit_scraper import RedditScraper

from preprocessing.data_preprocessor import DataPreprocessor

from executor.pipeline_executor import NewsPipelineExecutor

import os
from datetime import datetime

from news_scrapers.polygon_scraper import PolygonNewsScraper

TARGET_SCHEMA = {
    'headline': 'title',
    'url': 'url',
    'date': 'publishedAt',
    'source': 'source_name',
    'description': 'description',
    'article': 'content'
}

if __name__ == '__main__':
    search_term = "TSLA"
    date = "2024-09-28"

    config = {
        # "NewsAPI": {"api_key": "a9a44d097ae748db86084a7d71d72606", "search_term": search_term, "date_from": "2024-09-28", "date_to": "2024-10-28"},
        "Polygon": {"api_key": "Wnm7kh3Qcie9dbYOt3VjET6h5KrkRhpn", "search_term": search_term, "date_from": "2020-09-28", "date_to": "2021-10-28"},
        # "Bing": {"search_term": search_term, "date": date},
        # "Reddit": {"search_term": search_term, "date": date}
    }

    schema_mappings = {
        "NewsAPI": {
            'headline': 'title',
            'url': 'url',
            'date': 'publishedAt',
            'source': 'source',
            'description': 'description',
            'article': 'content'

        },
        "Polygon": {
            'headline': 'title',
            'url': 'article_url',
            'date': 'published_utc',
            'source': 'source',
            'description': 'description',
            'article': 'content'
        },
        "Bing": {
            'headline': 'title',
            'url': 'url',
            'date': 'datePublished',
            'source': 'provider.name',
            'description': 'summary',

        },
        "Reddit": {
            'headline': 'title',
            'url': 'url',
            'date': 'created_utc',
            'source': 'subreddit',
            'selftext': 'summary',

        }
    }

    scrapers = {
        "Polygon": {"scraper": PolygonNewsScraper(config["Polygon"]), "schema_mapping": schema_mappings["Polygon"]},
        # "NewsAPI": {"scraper": NewsAPIScraper(config["NewsAPI"]), "schema_mapping": schema_mappings["NewsAPI"]},
        # "Bing": {"scraper": BingScraper(config["Bing"]), "schema_mapping": schema_mappings["Bing"]},
        # "Reddit": {"scraper": RedditScraper(config["Reddit"]), "schema_mapping": schema_mappings["Reddit"]}
    }

    preprocessor = DataPreprocessor(TARGET_SCHEMA)
    output_path = f"/Users/leen/Downloads/news_data"
    pipeline = NewsPipelineExecutor(scrapers, preprocessor, output_path)
    pipeline.execute()
