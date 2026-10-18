"""
Fetches relevant football articles from Google News API and saves metadata.
"""

from gnews import GNews
import json
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

news = GNews(language='en', 
                    period='1d', 
                    start_date=None, 
                    end_date=None, 
                    max_results=2, # final max_results will be 5
                    max_retries=3)

base_league_queries = {
    "UEFA Champions League": "UEFA Champions League",
    "Premier League": '"Premier League" England football',
    "La Liga": '"La Liga" Spain football',
    "Serie A": '"Serie A" Italy football',
    "Bundesliga": '"Bundesliga" German football',
    "Ligue 1": '"Ligue 1" France football'
}

# final_topics = ["results", "injury", "transfer"]
topics = ["results", "injury"]


# Fetches articles via custom query prompts and returns metadata of each article associated with base league
def retrieve_articles():
    articles_by_league = {}

    for league, base_query in base_league_queries.items():
        # Each league has a total of 4 queries, base on it's own, and with topic
        built_queries = [
            base_query,
            *(f'{base_query} {topic}' for topic in topics)
        ]

        articles_by_league[league] = []

        # Store articles metadata and it's associated query
        for query in built_queries:
            for article in news.get_news(query):
                articles_by_league[league].append({
                    "query": query,
                    "article": article
                })
    
    return articles_by_league


# Saves populated dict article data into json
def save_articles(path):
    article_data = retrieve_articles()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(article_data, file, indent=4)


# Establishes that destination url is non google web url via various conditions
def is_publisher_url(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()

    return (
        parsed.scheme in {"http", "https"}
        and bool(host)
        and host != "google.com"
        and not host.endswith(".google.com")
    )


# Returns article publisher url via original source url
def resolve_source_url(source_url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page()

            page.goto(
                source_url,
                wait_until="domcontentloaded",
                timeout=30_000,
            )

            page.wait_for_url(
                is_publisher_url,
                wait_until="domcontentloaded",
                timeout=30_000,
            )

            return page.url
        finally:
            browser.close()









