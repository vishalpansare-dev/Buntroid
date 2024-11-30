import sqlite3

def connect_db():
    """Connect to the SQLite database (or create it if it doesn't exist)."""
    conn = sqlite3.connect("/Users/vishal_pansare/PycharmProjects/Buntroid/scripts/assistant_data.db")
    return conn

def setup_tables():
    """Set up the required tables for tasks, reminders, and notes."""
    conn = connect_db()
    cursor = conn.cursor()

    # Create Tasks Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    # Create Reminders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder TEXT NOT NULL,
            time INTEGER NOT NULL
        )
    """)

    # Create Notes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
