import sqlite3
import json
from dotenv import load_dotenv
from scripts.service import get_completed_news_summaries


db_path = 'database/football_news.db'

load_dotenv()

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

try:
    articles = get_completed_news_summaries(db_path)
    print(json.dumps(articles, indent=2, ensure_ascii=False))
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