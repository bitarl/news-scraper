import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import datetime


def scrape_news(search_term):
    # Bing News URL with the search term
        # Base URL for Bing News search
    base_url = "https://www.bing.com"

    # Construct the complete URL by appending the search term to the base URL
    url = base_url + "/news/search?q=" + search_term

    # Send GET request to the Bing News website
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all news articles
        articles = soup.find_all("div", class_="t_s")

        # Extract headlines, summaries, and URLs
        news_data = []
        for article in articles:
            # Extract headline
            headline_element = article.find("a")
            headline = headline_element.get_text() if headline_element else "No headline found"

            # Extract URL
            relative_url = headline_element["href"] if headline_element else ""
            full_url = base_url + relative_url

            summary = article.find("div", class_="snippet").get_text()
            
            url = article.find("a")["href"]
            date_time = article.find("span", class_="t_date").get_text() if article.find("span", class_="t_date") else ""
            
            news_data.append({"headline": headline, "summary": summary, "url": full_url, "date_time": date_time})

        return news_data
    else:
        # If request failed, print error message
        print(f"Failed to fetch news for '{search_term}'. Status code: {response.status_code}")
        return []

def analyze_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    
    # Get the sentiment polarity (-1 to 1)
    sentiment_polarity = blob.sentiment.polarity
    
    # Determine sentiment label based on polarity
    if sentiment_polarity > 0:
        sentiment_label = "Positive"
    elif sentiment_polarity < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    return sentiment_label, sentiment_polarity

def print_article(article):
    print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Date/Time: {article['date_time']}")
    print(f"Headline: {article['headline']}")
    print(f"Summary: {article['summary']}")
    print(f"URL: {article['url']}")
    print()

def print_sentiment(sentiment_label, sentiment_polarity):
    print(f"Sentiment: {sentiment_label} (Polarity: {sentiment_polarity:.2f})")

search_term = "Tesla"
news_articles = scrape_news(search_term)

if news_articles:
    print("===== News Articles =====")
    for idx, article in enumerate(news_articles, start=1):
        print(f"Article {idx}:")
        print_article(article)

        # Analyze sentiment of headline and summary
        headline_sentiment_label, headline_sentiment_polarity = analyze_sentiment(article["headline"])
        summary_sentiment_label, summary_sentiment_polarity = analyze_sentiment(article["summary"])

        print("Sentiment Analysis:")
        print(" - Headline:")
        print_sentiment(headline_sentiment_label, headline_sentiment_polarity)
        print(" - Summary:")
        print_sentiment(summary_sentiment_label, summary_sentiment_polarity)

        print("-" * 50)  # Separator between articles
else:
    print("No news articles found.")

# # Example usage:
# search_term = "Tesla"
# news_articles = scrape_news(search_term)

# if news_articles:
#     print("News Articles:")
#     for idx, article in enumerate(news_articles, start=1):
#         # Analyze sentiment of headline and summary
#         headline_sentiment_label, headline_sentiment_polarity = analyze_sentiment(article["headline"])
#         summary_sentiment_label, summary_sentiment_polarity = analyze_sentiment(article["summary"])

#         # Format output with sentiment analysis results
#         output = f"{idx}. {article['headline']} (Sentiment: {headline_sentiment_label}, Polarity: {headline_sentiment_polarity:.2f})\n"
#         output += f"   - {article['summary']} (Sentiment: {summary_sentiment_label}, Polarity: {summary_sentiment_polarity:.2f})\n"
#         output += f"   - URL: {article['url']}"
#         print(output)
# else:
#     print("No news articles found.")