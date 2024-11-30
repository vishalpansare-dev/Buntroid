from scripts.database import connect_db
import time

def add_reminder(reminder_text, time_in_seconds):
    """Add a reminder to the database."""
    reminder_time = int(time.time()) + time_in_seconds  # Calculate the future time
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (reminder, time) VALUES (?, ?)", (reminder_text, reminder_time))
    conn.commit()
    conn.close()

def check_reminders():
    """Check and retrieve reminders that are due."""
    current_time = int(time.time())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, reminder FROM reminders WHERE time <= ?", (current_time,))
    due_reminders = cursor.fetchall()

    # Remove due reminders from the database
    for reminder_id, _ in due_reminders:
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))

    conn.commit()
    conn.close()

    # Return only the reminder text
    return [reminder[1] for reminder in due_reminders]

def list_reminders():
    """List all reminders, including upcoming ones."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT reminder, time FROM reminders")
    reminders = cursor.fetchall()
    conn.close()

    # Convert to a readable format
    readable_reminders = []
    for reminder, reminder_time in reminders:
        time_remaining = max(0, reminder_time - int(time.time()))
        readable_reminders.append(f"{reminder} (in {time_remaining // 60} minutes)")

    return readable_reminders
