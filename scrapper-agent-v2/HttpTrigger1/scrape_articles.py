import requests
from bs4 import BeautifulSoup 

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

    print('\nPrinting article titles, URLs, and content...\n')

    # Initialize a string to collect all printed content
    all_content = ""

    for article in articles:
        # Check if the article contains a div with the class 'item-title'
        title_div = article.find('div', class_='item-title')
        if title_div:
            # Extract the title text
            title = title_div.get_text(strip=True)
            
            # Extract the URL (href attribute of the <a> tag)
            relative_url = article['href']
            full_url = f"{base_url}{relative_url}"  # Append base URL to relative URL
            
            # Prepare the content to print
            article_info = f"ARTICLE TITLE: {title}\nARTICLE URL: {full_url}\n"
            
            # Print the title and full URL
            print(article_info)
            
            # Add to the all_content string
            all_content += article_info
            
            # Send a GET request to the article URL
            article_response = requests.get(full_url)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            
            # Extract the body content (assumes articles are wrapped in a specific class like 'wysiwyg')
            body_div = article_soup.find('div', class_='wysiwyg')
            if body_div:
                body_content = body_div.get_text(separator="\n", strip=True)  # Get text with line breaks
                content_info = f"ARTICLE CONTENT:\n{body_content}\n"
                print(content_info)
                all_content += content_info
            else:
                no_content_message = "Content not found.\n"
                print(no_content_message)
                all_content += no_content_message
            
            separator = "\n" + "-" * 80 + "\n"
            print(separator)
            all_content += separator

    return all_content

# Call the function and store the returned content
articles_content = scrape_articles()
# Print the full content if needed
print(articles_content)
