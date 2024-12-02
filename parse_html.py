import json


html_file_path = f'/Users/leen/Downloads/news_data/apple_inc/20240506/bing/bing_dump_20240506.html'
with open(html_file_path, 'r') as file:
    response = file.read()


articles = response.split("</h1>")[1:]


parsed_articles = []


for article in articles:
    lines = article.split("\n")
    
    headline = lines[0].strip()
    source_date = lines[1].strip()
    content = lines[2].strip()
    
    article_data = {
        "headline": headline,
        "source_date": source_date,
        "content": content
    }

    parsed_articles.append(article_data)


parsed_articles_json = json.dumps(parsed_articles, indent=4)


print(parsed_articles_json)

file_path = "/Users/leen/Downloads/news_data/apple_inc/20240506/bing/parsed_articles.json"

# Write the JSON to the file
with open(file_path, "w") as outfile:
    outfile.write(parsed_articles_json)