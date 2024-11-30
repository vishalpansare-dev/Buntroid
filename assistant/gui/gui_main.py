import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import os
from assistant.automation.custom_scripts import  start_scheduled_scripts
from assistant.file_management.directory_manager import organize_files, compress_files
from assistant.file_management.file_manager import rename_files, delete_old_files
# from assistant.email_check import check_email

# Create the main application window
root = tk.Tk()
root.title("Home AI Assistant")
root.geometry("800x600")  # Width x Height

# Create the log area
log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
log_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

def log(message, level="info"):
    """Update the log area with messages."""
    log_area.insert(tk.END, f"[{level.upper()}] {message}\n")
    log_area.yview(tk.END)  # Auto-scroll to the bottom

def run_script_gui():
    """Run a script manually from the GUI."""
    script_path = "scripts/script1.py"  # Example script, can be dynamically chosen
    threading.Thread(target=run_single_script, args=(script_path,), daemon=True).start()

def check_email_gui():
    """Check email using the background process."""
    threading.Thread(target=check_email, daemon=True).start()

def organize_files_gui():
    """Organize files in the directory using file manager."""
    threading.Thread(target=organize_files, daemon=True).start()

def rename_files_gui():
    """Rename files in the directory using file manager."""
    threading.Thread(target=rename_files, daemon=True).start()

def compress_files_gui():
    """Compress files in the directory."""
    threading.Thread(target=compress_files, daemon=True).start()

def delete_old_files_gui():
    """Delete old files in the directory."""
    threading.Thread(target=delete_old_files, daemon=True).start()

def start_scheduled_scripts_gui():
    """Start scheduled scripts for automation."""
    threading.Thread(target=start_scheduled_scripts, daemon=True).start()

def show_message(title, message):
    """Show a message box with a custom message."""
    messagebox.showinfo(title, message)

# Add buttons to the window
btn_run_script = tk.Button(root, text="Run Script", command=run_script_gui)
btn_run_script.grid(row=1, column=0, padx=10, pady=10)

btn_check_email = tk.Button(root, text="Check Email", command=check_email_gui)
btn_check_email.grid(row=1, column=1, padx=10, pady=10)

btn_organize_files = tk.Button(root, text="Organize Files", command=organize_files_gui)
btn_organize_files.grid(row=2, column=0, padx=10, pady=10)

btn_rename_files = tk.Button(root, text="Rename Files", command=rename_files_gui)
btn_rename_files.grid(row=2, column=1, padx=10, pady=10)

btn_compress_files = tk.Button(root, text="Compress Files", command=compress_files_gui)
btn_compress_files.grid(row=3, column=0, padx=10, pady=10)

btn_delete_old_files = tk.Button(root, text="Delete Old Files", command=delete_old_files_gui)
btn_delete_old_files.grid(row=3, column=1, padx=10, pady=10)

btn_start_scheduled_scripts = tk.Button(root, text="Start Scheduled Scripts", command=start_scheduled_scripts_gui)
btn_start_scheduled_scripts.grid(row=4, column=0, padx=10, pady=10)

# Add information button to show user guide
btn_info = tk.Button(root, text="Show Info", command=lambda: show_message("Home AI Assistant", "Use the buttons to trigger automation tasks."))
btn_info.grid(row=4, column=1, padx=10, pady=10)

# Run the main loop of the application
root.mainloop()
