import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
import os
import json
import io

def analyze_sentiment(text):
    
    blob = TextBlob(text)
    
    
    sentiment_polarity = blob.sentiment.polarity
    
    
    if sentiment_polarity > 0:
        sentiment_label = "Positive"
    elif sentiment_polarity < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    return sentiment_label, sentiment_polarity


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
    

# def scrape_news(search_term):
#     # Base URL for Bing News search
#     base_url = "https://www.bing.com"

#     # Construct the complete URL by appending the search term to the base URL
#     url = base_url + "/news/search?q=" + search_term

#     # Send GET request to the Bing News website
#     response = requests.get(url)

#     # Check if request was successful
#     if response.status_code == 200:
#         # Parse the HTML content of the response
#         soup = BeautifulSoup(response.content, "html.parser")

#         # Find all news articles
#         articles = soup.find_all("div", class_="t_s")


#         # Extract headlines, summaries, URLs, and dates
#         news_data = []
#         i = 0 
#         for article in articles:
            
#             # Extract headline
#             headline_element = article.find("a")
#             headline = headline_element.get_text() if headline_element else "No headline found"

#             # Extract URL
#             relative_url = headline_element["href"] if headline_element else ""
#             full_url = base_url + relative_url

#             # Use sumy to summarize the article content
#             if full_url:
#                 article_text = get_article_text(full_url)
#                 if article_text:
#                     parser = PlaintextParser.from_string(article_text, Tokenizer("english"))
#                     summarizer = LsaSummarizer()
#                     summary_sentences = summarizer(parser.document, 3)  # Adjust the number of sentences for summary

#                     # Concatenate summary sentences into a single string
#                     summary = " ".join(str(sentence) for sentence in summary_sentences)

#                     # Try to find date/time information
#                     date_time_element = article.find("div", class_="snippet").find_next("span", class_="t_date")
#                     date_time = date_time_element.get_text() if date_time_element else "none"

#                     # Extract all links in the article
#                     links = [link["href"] for link in article.find_all("a", href=True)]
#                     article_output = {"headline": headline, "summary": summary, "urls": links, "date_time": date_time, "article_text": article_text}
#                     news_data.append(article)
                    
#                     source_dir='/Users/leen/Downloads/news_data/bing'
#                     date_dir = os.path.join(source_dir, date_time)
#                     os.makedirs(date_dir, exist_ok=True)

#                     filename = os.path.join(date_dir, f"bing_{date_time}_{i}.json")
#                     with open(filename, "a") as f:
#                         json.dump(article_output, f, indent=4)
#                         print(f"Data written to {filename}")
#                     i += 1
#                 else:
#                     print(f"Failed to fetch article content from '{full_url}'.")
#             else:
#                 print("Failed to extract URL for an article.")

#         return news_data
#     else:
#         # If request failed, print error message
#         print(f"Failed to fetch news for '{search_term}'. Status code: {response.status_code}")
#         return []

def scrape_news(search_term):
    # Base URL for Bing News search
    base_url = "https://www.bing.com"


    url = base_url + "/news/search?q=" + search_term


    response = requests.get(url)


    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find('a', class_='title').text.strip()
        description = soup.find('div', class_='snippet').text.strip()
        date = soup.find('span', attrs={'aria-label': True}).text.strip()
        article_output = {
                "headline": title,
                "summary": description,
                "date_time": date,
                # "article_text": article_text
            }
        print(article_output)
        # articles = soup.find_all("div", class_="t_s")

        source_dir = f'/Users/leen/Downloads/news_data/{search_term}/{datetime.now().strftime("%Y%m%d")}/bing'
        os.makedirs(source_dir, exist_ok=True)
        filename = os.path.join(source_dir, f"bing_article_output_{datetime.now().strftime('%Y%m%d')}.json")
        
        with open(filename, 'w') as f:
            json.dump(article_output, f, indent=4)
            print(f"Data written to {filename}")
        rticle_containers = soup.find_all('div', class_='t_s')

        # Initialize a list to store articles
        articles = []

        # Find all article containers
        article_containers = soup.find_all('div', class_='t_s')

        # Loop through each article container
        for container in article_containers:
            # Extract title
            title_elem = container.find('a', class_='title')
            title = title_elem.text.strip() if title_elem else None
            
            # Extract article content
            content_elem = container.find('div', class_='snippet')
            content = content_elem.text.strip() if content_elem else None
            
            # Extract date
            date_elem = container.find('span', attrs={'aria-label': True})
            date = date_elem.text.strip() if date_elem else None
            
            # Create dictionary for the article
            article_data = {
                "title": title,
                "content": content,
                "date": date
            }
            
            # Append article data to the list of articles
            articles.append(article_data)
        filename = os.path.join(source_dir, f"bing_all_articles_{datetime.now().strftime('%Y%m%d')}.json")
        # Write articles to JSON file
        with open(filename, 'w') as json_file:
            json.dump(articles, json_file, indent=4)
            # for idx, article in enumerate(articles, start=1):
                # Write the article's HTML content to the file
                # f.write(f"<h1>Article {idx}</h1>\n")
                # f.write(io.StringIO(response)(article) + "\n")
        
        # news_data = []
        # for i, article in enumerate(articles):

        #     title = soup.find('a', class_='title').text.strip()
        #     description = soup.find('div', class_='snippet').text.strip()
        #     date = soup.find('span', attrs={'aria-label': True}).text.strip()

            # article_output = {
            #     "headline": title,
            #     "summary": description,
            #     "date_time": date,
            #     # "article_text": article_text
            # }
            
        
            # articles.append(article_output)
            # print(article_output)

            # relative_url = headline_element["href"] if headline_element else ""
            # full_url = base_url + relative_url

            # # Use sumy to summarize the article content
            # if full_url:
            #     article_text = get_article_text(full_url)
            #     if article_text:
            #         parser = PlaintextParser.from_string(article_text, Tokenizer("english"))
            #         summarizer = LsaSummarizer()
            #         summary_sentences = summarizer(parser.document, 3)  # Adjust the number of sentences for summary

            #         # Concatenate summary sentences into a single string
            #         summary = " ".join(str(sentence) for sentence in summary_sentences)

            #         # Try to find date/time information
            #         date_time_element = article.find("div", class_="snippet").find_next("span", class_="t_date")
            #         date_time = date_time_element.get_text() if date_time_element else "none"

            #         # Extract all links in the article
            #         links = [link["href"] for link in article.find_all("a", href=True)]
            #         article_output = {"headline": headline, "summary": summary, "urls": links, "date_time": date_time, "article_text": article_text}
            # news_data.append(article_output)
                # else:
                #     print(f"Failed to fetch article content from '{full_url}'.")
            # else:
            #     print("Failed to extract URL for an article.")

        # Write all news data to a JSON file
        
    #     source_dir = f'/Users/leen/Downloads/news_data/{search_term}/{datetime.now().strftime("%Y%m%d")}/bing'
    #     os.makedirs(source_dir, exist_ok=True)
    #     filename = os.path.join(source_dir, f"bing_news_{datetime.now().strftime('%Y-%m-%d')}.json")
    #     with open(filename, "w") as f:
    #         # json.dump(news_data, f, indent=4)
    #         print(f"Data written to {filename}")

    #     # return news_data
    # else:
    #     # If request failed, print error message
    #     print(f"Failed to fetch news for '{search_term}'. Status code: {response.status_code}")
    #     return []

    
def print_article(article):
    print(f"Date/Time: {article['date_time']}")
    print(f"Headline: {article['headline']}")
    print("Summary:")
    for sentence in article['summary'].split(". "):  # Split by sentence endings
        print(f" - {sentence.strip()}")  # Remove leading/trailing whitespaces
    print(f"URL: {article['urls']}")
    print()

def print_sentiment(sentiment_label, sentiment_polarity):
    print(f"Sentiment: {sentiment_label} (Polarity: {sentiment_polarity:.2f})")

search_term = "hashi corp"
news_articles = scrape_news(search_term)

if news_articles:
    print("===== News Articles =====")
    for idx, article in enumerate(news_articles, start=1):
        print(f"Article {idx}:")
        print_article(article)

        # Analyze sentiment of headline and summary
        headline_sentiment_label, headline_sentiment_polarity = analyze_sentiment(article["headline"])
        summary_sentiment_label, summary_sentiment_polarity = analyze_sentiment(" ".join(article["summary"]))

        print("Sentiment Analysis:")
        print(" - Headline:")
        print_sentiment(headline_sentiment_label, headline_sentiment_polarity)
        print(" - Summary:")
        print_sentiment(summary_sentiment_label, summary_sentiment_polarity)

        print("-" * 50)  # Separator between articles
else:
    print("No news articles found.")