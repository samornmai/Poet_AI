import os
import sqlite3
import uuid
from pathlib import Path

import psycopg2
import psycopg2.extras

DB_PATH = Path(__file__).resolve().parent / "poet_studio.db"

POSTGRES_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "database": os.getenv("DB_NAME", "poet_studio"),
}


def _ensure_sqlite_schema(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            auth_token TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            genre TEXT NOT NULL,
            save_type TEXT NOT NULL,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    saved_stories_info = conn.execute("PRAGMA table_info(saved_stories)").fetchall()
    columns = {row[1] for row in saved_stories_info}
    if "save_type" not in columns:
        conn.execute("ALTER TABLE saved_stories ADD COLUMN save_type TEXT")
    if "user_id" not in columns:
        conn.execute("ALTER TABLE saved_stories ADD COLUMN user_id INTEGER")

    conn.execute(
        "UPDATE saved_stories SET save_type = 'story' WHERE save_type IS NULL OR save_type = ''"
    )
    conn.commit()


def _ensure_postgres_schema(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                auth_token TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS saved_stories (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                genre TEXT NOT NULL,
                save_type TEXT NOT NULL DEFAULT 'story',
                user_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    conn.commit()


def _connect_postgres():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    conn.autocommit = False
    _ensure_postgres_schema(conn)
    return conn


def _connect_sqlite():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _ensure_sqlite_schema(conn)
    return conn


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)

    try:
        return _connect_postgres()
    except Exception:
        return _connect_sqlite()


def _row_to_dict(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(row)


# =========================
# USERS
# =========================

def register_user(username, email, password):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if isinstance(conn, sqlite3.Connection):
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?,?,?)",
                (username, email, password),
            )
        else:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                (username, email, password),
            )

        conn.commit()
        return True
    except Exception as e:
        print("Register Error:", e)
        return False
    finally:
        if conn:
            conn.close()


def login_user(email, password):
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, password),
            )
            user = cursor.fetchone()
        else:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (email, password),
            )
            user = cursor.fetchone()

        if not user:
            return None

        token = str(uuid.uuid4())
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("UPDATE users SET auth_token=? WHERE id=?", (token, user["id"]))
        else:
            cursor.execute("UPDATE users SET auth_token=%s WHERE id=%s", (token, user["id"]))

        conn.commit()
        user = _row_to_dict(user)
        user["auth_token"] = token
        return user
    except Exception as e:
        print("Login Error:", e)
        return None
    finally:
        if conn:
            conn.close()


def verify_token(user_id, token):
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id=? AND auth_token=?", (user_id, token))
        else:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM users WHERE id=%s AND auth_token=%s", (user_id, token))

        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        print("Token Error:", e)
        return False
    finally:
        if conn:
            conn.close()


# =========================
# STORIES
# =========================

def save_story_to_db(title, content, genre, save_type, user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if isinstance(conn, sqlite3.Connection):
            cursor.execute(
                """
                INSERT INTO saved_stories
                (title, content, genre, save_type, user_id)
                VALUES (?,?,?,?,?)
                """,
                (title, content, genre, save_type, user_id),
            )
        else:
            cursor.execute(
                """
                INSERT INTO saved_stories
                (title, content, genre, save_type, user_id)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (title, content, genre, save_type, user_id),
            )

        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Save Error:", e)
        return None
    finally:
        if conn:
            conn.close()


def delete_story_from_db(story_id, user_id=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if user_id:
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("DELETE FROM saved_stories WHERE id=? AND user_id=?", (story_id, user_id))
            else:
                cursor.execute("DELETE FROM saved_stories WHERE id=%s AND user_id=%s", (story_id, user_id))
        else:
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("DELETE FROM saved_stories WHERE id=?", (story_id,))
            else:
                cursor.execute("DELETE FROM saved_stories WHERE id=%s", (story_id,))

        conn.commit()
        return True
    except Exception as e:
        print("Delete Error:", e)
        return False
    finally:
        if conn:
            conn.close()


# =========================
# FIX: USER STORIES
# =========================

def fetch_saved_stories(user_id=None):
    """Return story rows as dictionaries for both SQLite and MySQL-backed stores."""
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            if user_id is None:
                cursor.execute(
                    """
                    SELECT id, title, genre, save_type, content, user_id, timestamp
                    FROM saved_stories
                    ORDER BY id DESC
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT id, title, genre, save_type, content, user_id, timestamp
                    FROM saved_stories
                    WHERE user_id=?
                    ORDER BY id DESC
                    """,
                    (user_id,),
                )
            rows = cursor.fetchall()
            return [_row_to_dict(row) for row in rows]

        cursor = conn.cursor(dictionary=True)
        if user_id is None:
            cursor.execute(
                """
                SELECT id, title, genre, save_type, content, user_id, timestamp
                FROM saved_stories
                ORDER BY id DESC
                """
            )
        else:
            cursor.execute(
                """
                SELECT id, title, genre, save_type, content, user_id, timestamp
                FROM saved_stories
                WHERE user_id=%s
                ORDER BY id DESC
                """,
                (user_id,),
            )
        return cursor.fetchall()
    except Exception as e:
        print("Fetch Error:", e)
        return []
    finally:
        if conn:
            conn.close()


# =========================
# ADMIN FUNCTION (OPTIONAL)
# =========================

def fetch_all_stories():
    """Admin / no-token view"""
    return fetch_saved_stories(user_id=None)