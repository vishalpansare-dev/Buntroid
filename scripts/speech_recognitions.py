import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer


def initialize_recognition(model_path):
    """Initialize the Vosk model and microphone input."""
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    return recognizer


def recognize_speech(recognizer):
    """Listen and recognize speech using sounddevice."""
    recognized_text = None  # To store the recognized speech

    def callback(indata, frames, time, status):
        """Process the audio data and recognize speech."""
        nonlocal recognized_text  # To modify the recognized_text in the main function
        if status:
            print(status)

        # Convert indata (numpy array) to bytes
        indata_bytes = indata.tobytes()

        # Check if speech is recognized
        if recognizer.AcceptWaveform(indata_bytes):
            result = recognizer.Result()
            print(f"Recognized: {result}")
            recognized_text = result  # Store the recognized text

    # Start the input stream
    with sd.InputStream(channels=1, samplerate=16000, dtype='int16', callback=callback):
        print("Listening for commands...")

        # Continuously listen for speech until we get a result
        while recognized_text is None:
            sd.sleep(100)  # Sleep to avoid 100% CPU usage
        return recognized_text


def stop_recognition():
    """Stop the recognition."""
    pass
