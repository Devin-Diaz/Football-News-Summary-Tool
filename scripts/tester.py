import sqlite3
from resolve_source_urls import resolve_pending_urls

db_path = 'database/football_news.db'

conn = sqlite3.connect(db_path)

try:
    conn.execute("PRAGMA foreign_keys = ON")
    resolve_pending_urls(conn)
finally:
    conn.close()