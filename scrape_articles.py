import requests
from bs4 import BeautifulSoup

# Base URL of the website
base_url = 'https://a16zcrypto.com'
url = f'{base_url}/posts/'

# Send a GET request to the main posts page
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all article containers
articles = soup.find_all('a', href=True)  # Anchor tags with href attributes

print('\nPrinting ariticle titles, URLs, and content...\n')
for article in articles:
    # Check if the article contains a div with the class 'item-title'
    title_div = article.find('div', class_='item-title')
    if title_div:
        # Extract the title text
        title = title_div.get_text(strip=True)
        
        # Extract the URL (href attribute of the <a> tag)
        relative_url = article['href']
        full_url = f"{base_url}{relative_url}"  # Append base URL to relative URL
        
        # Print the title and full URL
        print(f"ARTICLE TITLE: {title}")
        print(f"ARTICLE URL: {full_url}")
        
        # Send a GET request to the article URL
        article_response = requests.get(full_url)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        # Extract the body content (assumes articles are wrapped in a specific class like 'wysiwyg')
        body_div = article_soup.find('div', class_='wysiwyg')
        if body_div:
            body_content = body_div.get_text(separator="\n", strip=True)  # Get text with line breaks
            print("ARTICLE CONTENT:")
            print(body_content)
        else:
            print("Content not found.")
        
        print("\n" + "-" * 80 + "\n")
