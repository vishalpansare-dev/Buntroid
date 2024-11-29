import os
import json
from datetime import datetime

TASKS_FILE = "tasks.json"

# Load existing tasks from a file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Add a new task
def add_task(task_name):
    tasks = load_tasks()
    task = {
        "name": task_name,
        "added_at": str(datetime.now())
    }
    tasks.append(task)
    save_tasks(tasks)

# List all tasks
def list_tasks():
    tasks = load_tasks()
    if tasks:
        return "\n".join([f"{idx + 1}. {task['name']} (added on {task['added_at']})" for idx, task in enumerate(tasks)])
    return "No tasks available."

# Delete a task
def delete_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        task = tasks.pop(task_index)
        save_tasks(tasks)
        return f"Task '{task['name']}' removed."
    return "Task not found."
