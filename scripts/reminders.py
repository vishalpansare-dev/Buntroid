# reminders.py

import time

reminders = []


def add_reminder(reminder, time_in_seconds):
    """Add a reminder that will trigger after a certain amount of time."""
    reminders.append({"reminder": reminder, "time": time_in_seconds})
    return f"Reminder set: {reminder} in {time_in_seconds} seconds."


def check_reminders():
    """Check if any reminders need to be triggered."""
    current_time = time.time()
    triggered_reminders = []
    for reminder in reminders:
        if current_time >= reminder["time"]:
            triggered_reminders.append(reminder["reminder"])
            reminders.remove(reminder)

    return triggered_reminders

