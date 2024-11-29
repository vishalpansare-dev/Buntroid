import sqlite3
from pathlib import Path

# Define the database file name
DB_FILE = Path("buntroid.db")

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_FILE)

def initialize_database():
    """Create tables if they don't already exist."""
    conn = connect_db()
    cursor = conn.cursor()

    # Define table creation queries
    queries = [
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            time_to_remind TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]

    # Execute all queries
    for query in queries:
        cursor.execute(query)

    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Execute a query and return the results."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    results = cursor.fetchall()
    conn.close()
    return results
