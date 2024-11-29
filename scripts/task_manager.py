import json
import os

# Define the file where tasks will be stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from a JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []  # Return an empty list if the file does not exist

def save_tasks():
    """Save tasks to a JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Load tasks when the program starts
tasks = load_tasks()

def add_task(task):
    """Add a new task to the task list."""
    tasks.append(task)
    save_tasks()  # Save tasks after adding
    return f"Task '{task}' added."

def list_tasks():
    # Assuming tasks are stored as a list of dictionaries
    tasks = load_tasks()  # Fetch tasks from wherever they're stored

    # If tasks is a list of dictionaries, you can extract the 'task' field (or whatever field holds the task name)
    task_strings = [task.get('task', 'Unnamed task') for task in tasks]

    return "\n".join(task_strings)  # Join the list of task names into a single string

def remove_task(task):
    """Remove a task from the list."""
    if task in tasks:
        tasks.remove(task)
        save_tasks()  # Save tasks after removing
        return f"Task '{task}' removed."
    else:
        return f"Task '{task}' not found."
