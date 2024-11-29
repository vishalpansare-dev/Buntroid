# gui.py

import tkinter as tk
from task_manager import list_tasks, add_task, delete_task

def update_task_list():
    """Update the task list on the GUI."""
    task_list.delete(1.0, tk.END)  # Clear current tasks
    tasks = list_tasks()  # Get tasks from the task manager
    task_list.insert(tk.END, tasks)  # Insert updated task list

def on_add_task():
    """Add a task from the input field."""
    task = task_input.get()
    if task:
        add_task(task)
        update_task_list()

def on_remove_task():
    """Remove a task from the input field."""
    task = task_input.get()
    if task:
        delete_task(task)
        update_task_list()

# Create the main window
window = tk.Tk()
window.title("Task Manager")

# Create UI elements
task_input = tk.Entry(window, width=50)
task_input.pack(pady=10)

add_button = tk.Button(window, text="Add Task", command=on_add_task)
add_button.pack(pady=5)

remove_button = tk.Button(window, text="Remove Task", command=on_remove_task)
remove_button.pack(pady=5)

task_list = tk.Text(window, height=10, width=50)
task_list.pack(pady=10)

# Start by updating the task list
update_task_list()

# Run the GUI
window.mainloop()
