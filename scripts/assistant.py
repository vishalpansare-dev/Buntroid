import logging

from scripts.db_helper import initialize_database
from scripts.gui import create_gui
from scripts.nlp import classify_intent, extract_entities

logging.basicConfig(filename='/Users/vishal_pansare/PycharmProjects/Buntroid/logs/assistant_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_interaction(action):
    """Logs the interaction to the log file."""
    logging.info(action)


def main():
    create_gui()


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


if __name__ == "__main__":
    initialize_database()
    # # log_interaction(f"Command: audio, Response: response")
    # main()
    # process_command("Remind me to email John tomorrow at 10 AM")
