"""
Main pipelone workflow for data creation & and presenting
"""

import json
import sqlite3

from football_news.config import (
    ARTICLE_METADATA_PATH,
    DATABASE_PATH,
    create_directories
)

from football_news.db_operations import (
    create_tables, 
    replace_articles,
    get_final_summarized_outputs,
    fetch_article_by_id
)

from football_news.retrieve_article_data import (
    save_base_articles_metadata,
    extract_article_full_text,
)

from football_news.resolve_source_urls import resolve_pending_urls_workflow
from football_news.invoke_llm import generate_article_summary_workflow


# Runs article summary workflow end-to-end
def run_news_pipeline():
    
    create_directories()

    save_base_articles_metadata(ARTICLE_METADATA_PATH)

    with open(ARTICLE_METADATA_PATH, encoding="utf-8") as file:
        article_data = json.load(file)

    # Avoid clearing existing data when retrieval returns nothing
    if not any(article_data.values()):
        raise ValueError("No articles retrieved; existing data was preserved")

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        create_tables(conn)
        replace_articles(conn, article_data)

        resolve_pending_urls_workflow(conn)
        extract_article_full_text(conn)
        generate_article_summary_workflow(conn)

        return {"status": "completed"}
    finally:
        conn.close()


# Returns current article summaries.
def get_completed_news_summaries():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    try:
        rows = get_final_summarized_outputs(conn)
        return [dict(row) for row in rows]
    finally:
        conn.close()


# display single article via it's ID
def get_article_by_id(article_id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    try:
        row = fetch_article_by_id(conn, article_id)
        return dict(row) if row is not None else None
    finally:
        conn.close()
