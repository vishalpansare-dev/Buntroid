import tkinter as tk
from tkinter import ttk
from scripts.nlp import process_command
from task_manager import list_tasks, add_task, remove_task
from reminders import add_reminder, check_reminders
from notes import add_note, list_notes, remove_note
from speech_recognitions import recognize_speech, initialize_recognition

def execute_voice_command(status_var):
    """Execute a voice command using the speech recognition module and update the status bar."""
    print("Listening for a voice command...")
    recognizer = initialize_recognition("/Users/vishal_pansare/PycharmProjects/Buntroid/models/vosk-model")
    recognized_text = recognize_speech(recognizer)
    if recognized_text:
        print(f"Recognized Command: {recognized_text}")
        process_command(recognized_text)
        status_var.set(f"Executed command: {recognized_text}")
    else:
        print("No command recognized.")
        status_var.set("Voice command not recognized.")

def update_task_list(task_list):
    """Update the task list on the GUI."""
    task_list.delete(1.0, tk.END)
    tasks = list_tasks()
    task_list.insert(tk.END, "\n".join(tasks))

def update_reminders_list(reminders_list):
    """Update the reminders list on the GUI."""
    reminders_list.delete(1.0, tk.END)
    reminders = check_reminders()
    reminders_list.insert(tk.END, "\n".join(reminders))

def update_notes_list(notes_list):
    """Update the notes list on the GUI."""
    notes_list.delete(1.0, tk.END)
    notes = list_notes()
    notes_list.insert(tk.END, "\n".join(notes))

def create_gui():
    """Create the main GUI for the assistant."""
    window = tk.Tk()
    window.title("Buntroid Assistant")
    window.geometry("800x600")

    # Status Bar
    status_var = tk.StringVar()
    status_var.set("Assistant ready.")
    status_bar = tk.Label(window, textvariable=status_var, relief="sunken", anchor="w")
    status_bar.pack(fill="x", padx=10, pady=5)

    # Tabs
    tab_control = ttk.Notebook(window)

    # Tasks Tab
    tasks_tab = ttk.Frame(tab_control)
    tab_control.add(tasks_tab, text="Tasks")

    task_input = tk.Entry(tasks_tab, width=50)
    task_input.pack(pady=10)

    task_list = tk.Text(tasks_tab, height=15, width=70)
    task_list.pack(pady=10)

    tk.Button(tasks_tab, text="Add Task", command=lambda: [add_task(task_input.get()), update_task_list(task_list)]).pack()
    tk.Button(tasks_tab, text="Remove Task", command=lambda: [remove_task(task_input.get()), update_task_list(task_list)]).pack()
    tk.Button(tasks_tab, text="Voice Command", command=lambda: execute_voice_command(status_var)).pack()  # Voice Command Button

    update_task_list(task_list)

    # Reminders Tab
    reminders_tab = ttk.Frame(tab_control)
    tab_control.add(reminders_tab, text="Reminders")

    reminder_input = tk.Entry(reminders_tab, width=50)
    reminder_input.pack(pady=10)

    reminder_time_input = tk.Entry(reminders_tab, width=10)
    reminder_time_input.pack(pady=5)

    reminders_list = tk.Text(reminders_tab, height=15, width=70)
    reminders_list.pack(pady=10)

    tk.Button(reminders_tab, text="Add Reminder",
              command=lambda: [add_reminder(reminder_input.get(), int(reminder_time_input.get())), update_reminders_list(reminders_list)]).pack()
    tk.Button(reminders_tab, text="Voice Command", command=lambda: execute_voice_command(status_var)).pack()  # Voice Command Button

    update_reminders_list(reminders_list)

    # Notes Tab
    notes_tab = ttk.Frame(tab_control)
    tab_control.add(notes_tab, text="Notes")

    note_input = tk.Entry(notes_tab, width=50)
    note_input.pack(pady=10)

    notes_list = tk.Text(notes_tab, height=15, width=70)
    notes_list.pack(pady=10)

    tk.Button(notes_tab, text="Add Note", command=lambda: [add_note(note_input.get()), update_notes_list(notes_list)]).pack()
    tk.Button(notes_tab, text="Remove Note", command=lambda: [remove_note(note_input.get()), update_notes_list(notes_list)]).pack()
    tk.Button(notes_tab, text="Voice Command", command=lambda: execute_voice_command(status_var)).pack()  # Voice Command Button

    update_notes_list(notes_list)

    # Add tabs to the window
    tab_control.pack(expand=1, fill="both")

    # Run the GUI
    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
