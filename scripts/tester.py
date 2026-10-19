import sqlite3
from resolve_source_urls import resolve_pending_urls
from retrieve_article_data import extract_article_full_text
from gnews import GNews

db_path = 'database/football_news.db'

conn = sqlite3.connect(db_path)

try:
    conn.execute("PRAGMA foreign_keys = ON")
    extract_article_full_text(conn)
finally:
    conn.close()

# news = GNews(language='en', 
#                     period='1d', 
#                     start_date=None, 
#                     end_date=None, 
#                     max_results=2, # final max_results will be 5
#                     max_retries=3)

# temp = news.get_full_article('https://sports.yahoo.com/articles/guler-huijsen-start-4-2-195000503.html')

# full_text = temp['text']


# print(full_text)