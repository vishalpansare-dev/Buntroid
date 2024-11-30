from scripts.database import connect_db

def add_task(task):
    """Add a task to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def remove_task(task):
    """Remove a task from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
    conn.commit()
    conn.close()

def list_tasks():
    """List all tasks from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT task FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return [task[0] for task in tasks]  # Return as a list of strings

if __name__ == "__main__":
    add_task("vishal")
    print(list_tasks())