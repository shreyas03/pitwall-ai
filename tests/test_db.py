import sqlite3
import os

DB_PATH = "Formula1.sqlite"

def test_db_file_exists():
    """Verify that the SQLite database file exists in the repository root."""
    assert os.path.exists(DB_PATH), f"Expected {DB_PATH} to exist."

def test_db_has_tables():
    """Ensure the SQLite database contains tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert len(tables) > 0, "Database exists but contains no tables."