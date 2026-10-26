"""
Fetches relevant football articles from Google News API and saves metadata.
"""

from gnews import GNews
import json
from gnews import NetworkError
import time
from football_news.db_operations import get_resolved_articles, store_full_text

news = GNews(language='en', 
                    period='7d', 
                    start_date=None, 
                    end_date=None, 
                    max_results=5,
                    max_retries=3)

base_league_queries = {
    "UEFA Champions League": "UEFA Champions League",
    "Premier League": '"Premier League" England football',
    "La Liga": '"La Liga" Spain football',
    "Serie A": '"Serie A" Italy football',
    "Bundesliga": '"Bundesliga" German football',
    "Ligue 1": '"Ligue 1" France football'
}

topics = ["results", "injury", "transfer"]

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
def save_base_articles_metadata(path):
    article_data = retrieve_articles()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(article_data, file, indent=4)


# Extracts full text from article via publisher URL
def extract_article_full_text(conn, delay_seconds=4):
    resolved_articles = get_resolved_articles(conn)

    for index, (article_id, publisher_url) in enumerate(resolved_articles):
        # Pause between attemps including failed extractions
        if index > 0:
            time.sleep(delay_seconds)
        
        try:
            full_article_obj = news.get_full_article(publisher_url)
            full_text = full_article_obj.get("text", "").strip()

        except NetworkError as error:
            print(f"Could not extract article {article_id}: {error}")
            continue

        if not full_text:
            print(f"No text extracted from article: {article_id}")
            continue

        store_full_text(conn, full_text, article_id)
        print(f"Saved full text for article: {article_id}")

