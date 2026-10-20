"""
Main pipelone workflow for data creation & and presenting
"""

# service.py
import json
import sqlite3

from scripts.db_operations import (
    create_tables, 
    store_articles,
    get_final_summarized_outputs,
)

from scripts.retrieve_article_data import (
    save_base_articles_metadata,
    extract_article_full_text,
)

from scripts.resolve_source_urls import resolve_pending_urls_workflow
from scripts.invoke_llm import generate_article_summary_workflow


# Runs article summary workflow end-to-end
def run_news_pipeline(json_path, db_path):
    json_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    save_base_articles_metadata(json_path)

    with open(json_path, encoding="utf-8") as file:
        article_data = json.load(file)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        create_tables(conn)
        store_articles(conn, article_data)

        resolve_pending_urls_workflow(conn)
        extract_article_full_text(conn)
        generate_article_summary_workflow(conn)

        return {"status": "completed"}
    finally:
        conn.close()


# Returns current article summaries.
def get_completed_news_summaries(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        rows = get_final_summarized_outputs(conn)
        return [dict(row) for row in rows]
    finally:
        conn.close()


