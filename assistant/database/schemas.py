import sqlite3

# Database file path
DB_PATH = "assistant.db"

def create_tables():
    """
    Create tables in the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Tasks Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT,
            scheduled_time TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create User Preferences Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            level TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create Script Execution Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS script_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script_name TEXT NOT NULL,
            status TEXT,
            output TEXT,
            executed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create Email Notifications Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
