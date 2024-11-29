import pyttsx3

def initialize_speech_engine():
    """Initialize the speech engine."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    return engine

def speak(engine, text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()
