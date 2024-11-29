import json
import queue
import sys

import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer

q = queue.Queue()
def initialize_recognition(model_path):
    """Initialize the Vosk model and microphone input."""
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    return recognizer


def recognize_speech(recognizer):
    """Listen and recognize speech using sounddevice."""
    recognized_text = None  # To store the recognized speech

    def callback(indata, frames, time, status):
        """Process audio stream and add it to the queue."""
        if status:
            print(f"Status: {status}", file=sys.stderr)
        q.put(bytes(indata))

        # Start the input stream
    with sd.InputStream(callback=callback, channels=1, samplerate=16000, dtype="int16"):
        print("Listening for commands...")
        while True:
            audio_data = q.get()  # Get audio data from the queue
            if recognizer.AcceptWaveform(audio_data):  # Process the audio data
                result = recognizer.Result()
                result_json = json.loads(result)
                if "text" in result_json:
                    return result_json["text"]  # Return the recognized text

def stop_recognition():
    """Stop the recognition."""
    pass
