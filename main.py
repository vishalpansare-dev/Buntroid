import pyttsx3
import speech_recognition as sr
from assistant.nlp_processor import generate_response
from assistant.file_manager import create_directory, delete_directory, search_file
from assistant.email_checker import check_emails
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)


# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to recognize speech from mic
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_sphinx(audio)  # Use pocketsphinx for offline recognition
        except sr.UnknownValueError:
            return "I didn't catch that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
        except sr.WaitTimeoutError:
            return "You didn't say anything."


# Process user commands
def process_command(command):
    if "check email" in command:
        emails = check_emails("your_email@gmail.com", "your_password")
        return "\n".join(emails)
    elif "create directory" in command:
        path = command.replace("create directory", "").strip()
        return create_directory(path)
    elif "delete directory" in command:
        path = command.replace("delete directory", "").strip()
        return delete_directory(path)
    elif "search file" in command:
        file_name = command.replace("search file", "").strip()
        results = search_file(file_name)
        return "\n".join(results)
    elif "generate text" in command:
        prompt = command.replace("generate text", "").strip()
        return generate_response(prompt)
    else:
        return "Sorry, I don't recognize this command."


# Main interactive loop
def interactive_agent():
    speak("Hello! I am your offline assistant. How can I help you today?")
    while True:
        command = recognize_speech().lower()
        print(f"You said: {command}")

        if "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day!")
            break

        response = process_command(command)
        print(f"AI: {response}")
        speak(response)


# Background tasks (if any)
def run_background_tasks():
    # Placeholder for task scheduling or other background tasks
    pass


# Start background tasks in a separate thread
threading.Thread(target=run_background_tasks, daemon=True).start()

# Run the interactive agent
if __name__ == "__main__":
    interactive_agent()
