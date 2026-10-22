"""
Handles resolving source google web URLs to actual article publisher URLs 
"""

from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from playwright.sync_api import Error as PlaywrightError
from football_news.db_operations import get_unresolved_articles, store_publisher_url

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


# Workflow for resolving and storing publsiher URLs via source URLs
def resolve_pending_urls_workflow(conn):
    articles = get_unresolved_articles(conn)

    for article_id, source_url in articles:
        try:
            publisher_url = resolve_source_url(source_url)
        except PlaywrightError as error:
            print(f"Could not resolve article {article_id}: {error}")
            continue

        store_publisher_url(conn, publisher_url, article_id)
        print(f"Saved publsiher URL for article {article_id}")

