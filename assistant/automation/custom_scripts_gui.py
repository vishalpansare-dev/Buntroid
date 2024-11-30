import tkinter as tk

from assistant.automation.custom_scripts import resume_script, pause_script, manual_trigger_script


class SchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home AI Assistant - Task Scheduler")

        # Example buttons for controlling scripts
        self.create_buttons()

    def create_buttons(self):
        # Manually trigger a script
        self.trigger_button = tk.Button(self, text="Run Script1 Now", command=self.run_script_now)
        self.trigger_button.pack()

        # Pause and resume controls
        self.pause_button = tk.Button(self, text="Pause Script1", command=self.pause_script1)
        self.pause_button.pack()

        self.resume_button = tk.Button(self, text="Resume Script1", command=self.resume_script1)
        self.resume_button.pack()

        # Add more controls as needed...

    def run_script_now(self):
        manual_trigger_script("scripts/script1.py")

    def pause_script1(self):
        pause_script("scripts/script1.py")

    def resume_script1(self):
        resume_script("scripts/script1.py")


# Running the GUI
app = SchedulerGUI()
app.mainloop()
