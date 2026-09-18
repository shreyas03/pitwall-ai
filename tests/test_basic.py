import sqlite3
import os

def test_database_connection():
    """Verify that a temporary SQLite database initializes properly."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, metric TEXT)")
    cursor.execute("INSERT INTO test_table (metric) VALUES ('pitwall')")
    conn.commit()
    
    cursor.execute("SELECT metric FROM test_table WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row[0] == "pitwall"

def test_environment_sanity():
    """Basic sanity check."""
    assert 1 + 1 == 2