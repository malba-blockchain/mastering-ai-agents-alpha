import logging
from scrape_articles import scrape_articles

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #Execute the article scraper from the function
    articles = scrape_articles()

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. {articles}")
    else:
        return func.HttpResponse(
             f"Scrapper function successfully executed. {articles}",
             status_code=200
        )
