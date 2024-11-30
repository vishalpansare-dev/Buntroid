
tasks = []

def add_task(task):
    tasks.append(task)
    return f"Task '{task}' added successfully!"

def list_tasks():
    return tasks if tasks else "No tasks available."
