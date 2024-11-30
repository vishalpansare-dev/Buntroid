from db_helper import execute_query
import datetime

LOG_FILE = "buntroid.log"

def log_event(event):
    """Log an event to the database and a log file."""
    # Save to database
    query = "INSERT INTO logs (event) VALUES (?);"
    execute_query(query, (event,))

    # Save to log file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"[{timestamp}] {event}\n")

def get_logs(limit=100):
    """Retrieve the most recent logs from the database."""
    query = f"SELECT event, timestamp FROM logs ORDER BY timestamp DESC LIMIT {limit};"
    results = execute_query(query)
    return [{"event": row[0], "timestamp": row[1]} for row in results]
