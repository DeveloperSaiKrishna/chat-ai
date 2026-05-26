import sqlite3

DB_PATH = "notes.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_note(filename: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (filename, content) VALUES (?, ?)", (filename, content)
    )

    conn.commit()
    note_id = cursor.lastrowid
    conn.close()

    return note_id


def get_note(note_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, filename, content FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()

    conn.close()
    return row


def get_notes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, filename, created_at FROM notes ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]
