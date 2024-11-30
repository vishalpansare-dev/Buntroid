import spacy
from task_manager import add_task, remove_task, list_tasks
from reminders import add_reminder
import dateparser
from datetime import datetime

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')


def process_command(command):
    """Process the command and take appropriate action."""

    # Step 1: Classify the intent of the command
    intent = classify_intent(command.lower())

    # Step 2: Extract entities from the command
    entities = extract_entities(command)

    # Step 3: Act based on the intent and entities
    if intent == "reminder":
        # Extract details for the reminder (like time and description)
        reminder = entities.get('TIME', 'No time specified')
        person = entities.get('PERSON', 'Unknown person')
        print(f"Setting a reminder for {person} at {reminder}")
        # You can call the add_reminder function here

    elif intent == "task":
        # Handle task-related commands
        print(f"Adding task: {command}")
        # You can call the add_task function here

    elif intent == "note":
        # Handle note-related commands
        print(f"Adding note: {command}")
        # You can call the add_note function here

    elif intent == "email":
        # Handle email-related commands
        print(f"Preparing to send email...")
        # You can call the send_email function here

    else:
        print("Sorry, I didn't understand that command.")



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
