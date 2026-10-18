import json
import sqlite3
from pathlib import Path

from db import create_tables, store_articles
from scripts.tools import save_articles

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)

    json_path = DATA_DIR / "tester_data.json"
    db_path = DB_DIR / "football_news.db"

    save_articles(json_path)

    with open(json_path, encoding="utf-8") as file:
        article_data = json.load(file)

    conn = sqlite3.connect(db_path)

    try:
        conn.execute("PRAGMA foreign_keys = ON")
        create_tables(conn)
        store_articles(conn, article_data)
        print("Articles stored successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()