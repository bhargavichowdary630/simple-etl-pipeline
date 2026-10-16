import sqlite3

DB_NAME = "posts.db"


def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def setup_database():
    """Create tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            title       TEXT NOT NULL,
            body        TEXT NOT NULL,
            word_count  INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rejected_records (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_data    TEXT NOT NULL,
            reason      TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def insert_post(post):
    """Insert a single validated post record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO posts (id, user_id, title, body, word_count)
        VALUES (:id, :user_id, :title, :body, :word_count)
    """, post)
    conn.commit()
    conn.close()


def insert_rejected(raw_data, reason):
    """Insert a rejected record with the reason it failed validation."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rejected_records (raw_data, reason)
        VALUES (?, ?)
    """, (str(raw_data), reason))
    conn.commit()
    conn.close()