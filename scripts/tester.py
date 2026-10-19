import sqlite3
from resolve_source_urls import resolve_pending_urls
from retrieve_article_data import extract_article_full_text
from db_operations import get_completed_entries
from prompts import ARTICLE_SUMMARY_INSTRUCTIONS
from invoke_llm import build_article_input, invoke_llm, generate_article_summary_workflow
from gnews import GNews
from openai import OpenAI
from dotenv import load_dotenv


db_path = 'database/football_news.db'

load_dotenv()

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

openai_client = OpenAI()

articles = get_completed_entries(conn)

try:
    conn.execute("PRAGMA foreign_keys = ON")
    generate_article_summary_workflow(conn)
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