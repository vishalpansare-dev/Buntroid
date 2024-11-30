import os
import shutil
import sqlite3
from datetime import datetime, timedelta

DB_PATH = "/Users/vishal_pansare/PycharmProjects/Buntroid/assistant/database/assistant.db"

def connect_db():
    """Establish a database connection."""
    return sqlite3.connect(DB_PATH)

def insert_task(name, description, status, scheduled_time):
    """Insert a new task into the tasks table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (name, description, status, scheduled_time)
        VALUES (?, ?, ?, ?)
    """, (name, description, status, scheduled_time))
    conn.commit()
    conn.close()

def get_tasks():
    """Retrieve all tasks from the tasks table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, status):
    """Update the status of a task."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (status, datetime.now(), task_id))
    conn.commit()
    conn.close()

def insert_log(message, level="info"):
    """Insert a log entry into the logs table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (message, level)
        VALUES (?, ?)
    """, (message, level))
    conn.commit()
    conn.close()

def insert_script_log(script_name, status, output):
    """Insert a log entry for a script execution into the script_logs table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO script_logs (script_name, status, output)
        VALUES (?, ?, ?)
    """, (script_name, status, output))
    conn.commit()
    conn.close()

def insert_email_notification(email, subject, body):
    """Insert a new email notification into the email_notifications table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO email_notifications (email, subject, body)
        VALUES (?, ?, ?)
    """, (email, subject, body))
    conn.commit()
    conn.close()

def get_logs():
    """Retrieve all logs from the logs table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    conn.close()
    return logs

BACKUP_DIR = "/Users/vishal_pansare/PycharmProjects/Buntroid/assistant/database/backups/"

def create_backup():
    """
    Create a backup of the SQLite database.
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Generate a unique backup file name based on the current date and time
    backup_filename = f"assistant_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        # Copy the database file to the backup location
        shutil.copy(DB_PATH, backup_path)
        print(f"Backup created successfully: {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {str(e)}")

def cleanup_old_database_entries():
    """
    Cleanup database entries older than a certain number of days (e.g., 30 days).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

    # Delete logs older than 30 days
    cursor.execute("DELETE FROM logs WHERE timestamp < ?", (cutoff_date,))
    cursor.execute("DELETE FROM script_logs WHERE executed_at < ?", (cutoff_date,))
    cursor.execute("DELETE FROM email_notifications WHERE sent_at < ?", (cutoff_date,))

    conn.commit()
    conn.close()

    print("Old database entries cleaned up successfully!")
