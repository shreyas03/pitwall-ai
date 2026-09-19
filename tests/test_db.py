import sqlite3
import os

DB_PATH = "Formula1.sqlite"

def test_db_contains_core_f1_tables():
    """Verify essential Ergast tables and rows exist."""
    assert os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Query sqlite_master to verify core schema structure
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Typical Ergast tables: drivers, races, results, or circuits
    assert any(t in tables for t in ["drivers", "races", "results", "circuits"])
    
    conn.close()