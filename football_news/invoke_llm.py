"""
Handles LLM related work for article summarization
"""


import json
from football_news.prompts import ARTICLE_SUMMARY_INSTRUCTIONS
from openai import OpenAI
import sqlite3
from typing import Literal
from pydantic import BaseModel
from football_news.db_operations import get_completed_entries, store_article_summary


# Stores metadata regarding LLM output
class ArticleSummary(BaseModel):
    serve: bool
    reason: Literal[
        "ok",
        "non_english",
        "unusable_content",
        "content_mismatch",
        "insufficient_information",
    ]
    summary: str | None


# Format of article prior LLM invocation
def build_article_input(article):
    return json.dumps(
        {
            "title": article["title"],
            "publisher": article["publisher"],
            "publisher_url": article["publisher_url"],
            "published_at": article["published_at"],
            "description": article["description"],
            "full_text": article["full_text"],
        },
        ensure_ascii=False,
        indent=2,
    )


# Invokes LLM with final outputs built out
def invoke_llm(client: OpenAI, article_input: str) -> ArticleSummary:
    
    response = client.responses.parse(
        model="gpt-5.6-luna",
        reasoning={"effort": "none"},
        instructions=ARTICLE_SUMMARY_INSTRUCTIONS,
        input=article_input,
        text_format=ArticleSummary,
        max_output_tokens=500,
        store=False,
    )

    result = response.output_parsed

    if response.status != "completed" or result is None:
        raise RuntimeError("No completed structured response recieved.")

    if result.serve:
        if result.reason != "ok" or not result.summary or not result.summary.strip():
            raise ValueError("Accepted article has an invalid summary response.")
    elif result.reason == "ok" or result.summary is not None:
        raise ValueError("Rejected article has an inconsistent response.")

    return result


# Full flow generating and summarizing each articles content
def generate_article_summary_workflow(conn):
    conn.row_factory = sqlite3.Row
    articles = get_completed_entries(conn)
    with OpenAI() as client:
        for article in articles:
            article_input = build_article_input(article)
            result = invoke_llm(client, article_input)

            if result.serve:
                store_article_summary(
                    conn,
                    result.summary,
                    article["id"],
                )
                print(f"Saved summary for: {article['title']}")
            else:
                print(f"Rejected article {article['id']}: {result.reason}")

