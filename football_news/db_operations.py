"""
Database queries for creating schema and storing data
"""

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            source_url TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            published_at TEXT,
            publisher TEXT,
            description TEXT,
            full_text TEXT,
            summary TEXT
        );

        CREATE TABLE IF NOT EXISTS article_matches (
            article_id INTEGER NOT NULL,
            competition TEXT NOT NULL,
            query TEXT NOT NULL,
            FOREIGN KEY (article_id) REFERENCES articles(id),
            UNIQUE (article_id, competition, query)
        );
    """)


# Stores article metadata and common articles via different search query to avoid duplicates
def store_articles(conn, article_data: dict):
    with conn:
        for league, entries in article_data.items():
            for entry in entries:
                article = entry["article"]
                query = entry["query"]

                # Only stores unique articles via source url
                conn.execute("""
                    INSERT INTO articles (
                        source_url, title, published_at,
                        publisher, description
                    )
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(source_url) DO NOTHING
                """, (
                    article["url"],
                    article["title"],
                    article.get("published date"),
                    article.get("publisher", {}).get("title"),
                    article.get("description"),
                ))

                # Finds existing article ID to associate with different search query, hence article search match
                article_id = conn.execute("""
                    SELECT id FROM articles WHERE source_url = ?
                """, (article["url"],)).fetchone()[0]

                conn.execute("""
                    INSERT INTO article_matches (
                        article_id, competition, query
                    )
                    VALUES (?, ?, ?)
                    ON CONFLICT(article_id, competition, query)
                    DO NOTHING
                """, (article_id, league, query))


# Resets data in database in preperation for new batch of articles
def replace_articles(conn, article_data):
    with conn:
        # Delete child records before their referenced articles
        conn.execute("DELETE FROM article_matches")
        conn.execute("DELETE FROM articles")
        store_articles(conn, article_data)


# Fetch articles by ID
def fetch_article_by_id(conn, article_id):
    return conn.execute("""
        SELECT id, title, publisher, publisher_url, published_at, summary
        FROM articles
        WHERE id = ?
            AND summary IS NOT NULL
    """, (article_id,)).fetchone()


# Fetch entries where publisher url is unresolved
def get_unresolved_articles(conn):
    return conn.execute("""
        SELECT id, source_url
        FROM articles
        WHERE publisher_url IS NULL
        ORDER BY id
    """).fetchall()


# Saves publisher url to respective entry
def store_publisher_url(conn, publisher_url, article_id):
    with conn:
        conn.execute("""
            UPDATE articles
            SET publisher_url = ?
            WHERE id = ?
        """, (publisher_url, article_id))


# Fetches all articles with resolved publisher url
def get_resolved_articles(conn):
    return conn.execute("""
        SELECT id, publisher_url
        FROM articles
        WHERE publisher_url IS NOT NULL
            AND full_text IS NULL
        ORDER BY id
        """).fetchall()


# Stores full text to respective article 
def store_full_text(conn, full_text, article_id):
    with conn:
        conn.execute("""
            UPDATE articles
            SET full_text = ?
            WHERE id = ?
        """, (full_text, article_id))


# Fetch articles with populated full text
def get_completed_entries(conn):
    return conn.execute("""
        SELECT id, publisher, publisher_url, published_at, 
               title, description, full_text
        FROM articles
        WHERE full_text IS NOT NULL
            AND TRIM(full_text) != ''
            AND summary IS NULL
        ORDER BY id
    """).fetchall()


# Save article summary
def store_article_summary(conn, summary, article_id):
    with conn:
        conn.execute("""
            UPDATE articles
            SET summary = ?
            WHERE id = ?
        """, (summary, article_id))


# Will retrieve all finalized summary articles for user
def get_final_summarized_outputs(conn):
    return conn.execute("""
        SELECT id, title, publisher, publisher_url,
               published_at, summary
        FROM articles
        WHERE summary IS NOT NULL
          AND TRIM(summary) != ''
        ORDER BY id DESC
    """).fetchall()


