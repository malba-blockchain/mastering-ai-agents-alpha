import requests
import logging
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def scrape_articles():
    # Base URL of the website
    base_url = 'https://a16zcrypto.com'
    url = f'{base_url}/posts/'

    # Send a GET request to the main posts page
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article containers
    articles = soup.find_all('a', href=True)  # Anchor tags with href attributes

    # Initialize a list to collect article data
    articles_data = []

    for article in articles:
        # Check if the article contains a div with the class 'item-title'
        title_div = article.find('div', class_='item-title')
        if title_div:
            # Extract the title text
            title = title_div.get_text(strip=True)
            
            # Extract the URL (href attribute of the <a> tag)
            relative_url = article['href']
            full_url = f"{base_url}{relative_url}"  # Append base URL to relative URL
            
            # Initialize the article dictionary
            article_dict = {
                "title": title,
                "url": full_url,
                "content": None
            }
            
            # Send a GET request to the article URL
            article_response = requests.get(full_url)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            
            # Extract the body content (assumes articles are wrapped in a specific class like 'wysiwyg')
            body_div = article_soup.find('div', class_='wysiwyg')
            if body_div:
                body_content = body_div.get_text(separator="\n", strip=True)  # Get text with line breaks
                article_dict["content"] = body_content
            else:
                article_dict["content"] = "Content not found."
            
            # Append the article data to the list
            articles_data.append(article_dict)

    # Return the list of articles as JSON
    return json.dumps(articles_data, ensure_ascii=False, indent=4)

# Call the function and save the JSON content
articles_json = scrape_articles()

# Save the JSON to a file
with open("articles.json", "w", encoding="utf-8") as json_file:
    json_file.write(articles_json)

# Print the JSON content to the console
print(articles_json)
