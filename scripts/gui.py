import tkinter as tk

from scripts.voice import voice_mode
from task_manager import list_tasks, add_task, remove_task
from reminders import add_reminder, check_reminders
from notes import add_note, list_notes, remove_note

def update_task_list(task_list):
    """Update the task list on the GUI."""
    task_list.delete(1.0, tk.END)  # Clear the current list
    tasks = list_tasks()  # Get tasks from task_manager module
    task_list.insert(tk.END, tasks)  # Display tasks in the list

def update_notes_list(notes_list):
    """Update the notes list on the GUI."""
    notes_list.delete(1.0, tk.END)  # Clear the current list
    notes = list_notes()  # Get notes from notes module
    notes_list.insert(tk.END, notes)  # Display notes in the list

def update_reminders_list(reminders_list):
    """Update the reminders list on the GUI."""
    reminders_list.delete(1.0, tk.END)  # Clear the current list
    reminders = check_reminders()  # Get reminders from reminders module
    reminders_list.insert(tk.END, "\n".join(reminders))  # Display reminders in the list

# Task-related functions
def on_add_task(task_input, task_list):
    task = task_input.get()  # Get task from input field
    if task:
        add_task(task)  # Add the task using add_task from task_manager
        update_task_list(task_list)  # Refresh task list on the GUI

def on_remove_task(task_input, task_list):
    task = task_input.get()  # Get task from input field
    if task:
        remove_task(task)  # Remove the task using remove_task from task_manager
        update_task_list(task_list)  # Refresh task list on the GUI

# Reminder-related functions
def on_add_reminder(reminder_input, reminder_time_input, reminders_list):
    reminder = reminder_input.get()  # Get reminder from input field
    try:
        time_in_seconds = int(reminder_time_input.get())  # Get reminder time in seconds
        if reminder:
            add_reminder(reminder, time_in_seconds)  # Add reminder using add_reminder from reminders
            update_reminders_list(reminders_list)  # Refresh reminders list on the GUI
    except ValueError:
        pass  # If input isn't a valid integer, ignore

# Notes-related functions
def on_add_note(note_input, notes_list):
    note = note_input.get()  # Get note from input field
    if note:
        add_note(note)  # Add the note using add_note from notes
        update_notes_list(notes_list)  # Refresh notes list on the GUI

def on_remove_note(note_input, notes_list):
    note = note_input.get()  # Get note from input field
    if note:
        remove_note(note)  # Remove the note using remove_note from notes
        update_notes_list(notes_list)  # Refresh notes list on the GUI

# Create the main window
def on_voice_command():
    """Function to handle the voice command button press"""
    voice_mode();

def create_gui():
    """Create the GUI with all necessary components"""
    window = tk.Tk()
    window.title("Task and Reminder Manager with Voice Interaction")

    # Task management UI elements
    task_input = tk.Entry(window, width=50)
    task_input.pack(pady=10)

    add_task_button = tk.Button(window, text="Add Task", command=lambda: on_add_task(task_input))
    add_task_button.pack(pady=5)

    task_list = tk.Text(window, height=10, width=50)
    task_list.pack(pady=10)

    # Reminder management UI elements
    reminder_input = tk.Entry(window, width=50)
    reminder_input.pack(pady=10)

    add_reminder_button = tk.Button(window, text="Add Reminder", command=lambda: on_add_reminder(reminder_input))
    add_reminder_button.pack(pady=5)

    # Voice command button
    voice_command_button = tk.Button(window, text="Voice Command", command=on_voice_command)
    voice_command_button.pack(pady=10)

    window.mainloop()
