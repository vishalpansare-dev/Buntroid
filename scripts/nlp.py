import spacy
from task_manager import add_task, remove_task, list_tasks
from reminders import add_reminder
import dateparser
from datetime import datetime

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')


def process_command(command):
    # Process the command with spaCy NLP
    doc = nlp(command.lower())

    # Check for task-related actions
    if "task" in command:
        if "add" in command:
            task_name = extract_task_name(doc)
            if task_name:
                add_task(task_name)
                return f"Task '{task_name}' added!"
            return "Please specify the task name."
        elif "remove" in command:
            task_name = extract_task_name(doc)
            if task_name:
                remove_task(task_name)
                return f"Task '{task_name}' removed!"
            return "Please specify the task name to remove."

    # Check for reminder-related actions
    elif "reminder" in command:
        if "add" in command:
            reminder_text = extract_reminder(doc)
            time_in_seconds = extract_time(doc)
            if reminder_text and time_in_seconds:
                add_reminder(reminder_text, time_in_seconds)
                return f"Reminder set: {reminder_text} in {time_in_seconds} seconds!"
            return "Please specify the reminder text and time."

    # If no recognized action
    return "Sorry, I didn't understand that command."


def extract_task_name(doc):
    # Extracts the task name based on noun chunks or entities
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'dobj':  # Direct object typically contains the task name
            return chunk.text
    return None


def extract_reminder(doc):
    # Extracts reminder text (just the first noun chunk for simplicity)
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'dobj':
            return chunk.text
    return None


def extract_time(doc):
    # Look for time-related entities
    for ent in doc.ents:
        if ent.label_ == "TIME" or ent.label_ == "DATE":
            # Try parsing a human-readable time string
            time_str = ent.text
            parsed_time = dateparser.parse(time_str)

            if parsed_time:
                # Convert the parsed time to seconds from now
                delta = parsed_time - datetime.now()
                return int(delta.total_seconds())
    return None


def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_] = ent.text
    return entities
def classify_intent(command):
    """Classify the intent of the command."""
    if "remind me" in command or "set reminder" in command:
        return "reminder"
    elif "add task" in command or "remove task" in command:
        return "task"
    elif "create note" in command or "add note" in command:
        return "note"
    elif "send email" in command:
        return "email"
    else:
        return "unknown"


if __name__ == "__main__":

    # Example
    command = "Remind me to call John tomorrow at 3 PM"
    entities = extract_entities(command)
    print(entities)
