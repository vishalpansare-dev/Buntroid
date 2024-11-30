
reminders = []

def add_reminder(reminder):
    reminders.append(reminder)
    return f"Reminder '{reminder}' set successfully!"

def list_reminders():
    return reminders if reminders else "No reminders set."
