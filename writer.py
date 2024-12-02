import json

def parse_article_file(file_path):
    article_output = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Headline:"):
                article_output["headline"] = line[len("Headline:"):].strip()
            elif line.startswith("Summary:"):
                article_output["summary"] = line[len("Summary:"):].strip()
            elif line.startswith("URLs:"):
                article_output["urls"] = line[len("URLs:"):].strip()
            elif line.startswith("Date/Time:"):
                article_output["date_time"] = line[len("Date/Time:"):].strip()
            elif line.startswith("Article Text:"):
                article_output["article_text"] = line[len("Article Text:"):].strip()
    return article_output

def write_to_json(parsed_data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(parsed_data, json_file, indent=4)


# article_file_name = "bing_news_2024-05-06.json"
# article_file_path = f'/Users/leen/Downloads/news_data/bing/{article_file_name}'
# parsed_article = parse_article_file(article_file_path)
# output_file_path = f"/Users/leen/Downloads/news_data/bing/clean_{article_file_name}"
# write_to_json(parsed_article, output_file_path)
        
def parse_article_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Initialize variables to store article data
    headline = ''
    summary = ''
    urls = []
    date_time = ''
    article_text = ''

    # Iterate over each line in the file
    for line in lines:
        # Check if the line contains a colon
        if ':' in line:
            # Split the line into prefix and content
            prefix, content = line.strip().split(':', 1)
            
            # Update variables based on prefix
            if prefix == 'Headline':
                headline = content.strip()
            elif prefix == 'Summary':
                summary = content.strip()
            elif prefix == 'URL':
                urls.append(content.strip())
            elif prefix == 'Date-Time':
                date_time = content.strip()
            elif prefix == 'Article':
                # Remove leading and trailing whitespace and append to article text
                article_text += content.strip() + '\n'
        else:
            # If the line doesn't contain a colon, it might be a continuation of the article text
            article_text += line.strip() + '\n'

    # Construct the output dictionary
    article_output = {"headline": headline, "summary": summary, "urls": urls, "date_time": date_time, "article_text": article_text}

    return article_output

# Test the parsing function
filename = '/Users/leen/Downloads/news_data/bing/bing_news_2024-05-06.json'
article_data = parse_article_file(filename)
print(article_data)
