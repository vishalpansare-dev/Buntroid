import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import os
import json
from utils.logger import log


class SpeechToText:
    def __init__(self, use_vosk=True, vosk_model_path="/Users/vishal_pansare/PycharmProjects/BB-BuntysBuntroid/model/vosk-model-en-in-0.5", wake_word="hey"):
        """
        Initialize the SpeechToText module with options for using Vosk for offline recognition.

        Args:
            use_vosk (bool): Whether to use Vosk for offline recognition.
            vosk_model_path (str): Path to the Vosk model directory.
            wake_word (str): Wake word to activate the assistant.
        """
        self.use_vosk = use_vosk
        self.wake_word = wake_word.lower()
        self.vosk_recognizer = None

        if use_vosk:
            if not os.path.exists(vosk_model_path):
                log(f"Vosk model not found at {vosk_model_path}. Please download and place it correctly.", "error")
                raise FileNotFoundError(f"Vosk model not found at {vosk_model_path}")
            self.vosk_model = Model(vosk_model_path)
            self.vosk_recognizer = KaldiRecognizer(self.vosk_model, 16000)

    def listen(self, duration=5, samplerate=16000):
        """
        Capture audio from the microphone using sounddevice.

        Args:
            duration (int): Duration in seconds to capture audio.
            samplerate (int): Sampling rate for the audio capture.

        Returns:
            np.ndarray or None: Captured audio as a NumPy array or None if an error occurs.
        """
        log("Listening for audio input...", "info")
        try:
            audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
            sd.wait()
            log("Audio input captured successfully.", "info")
            return audio
        except Exception as e:
            log(f"Error capturing audio: {e}", "error")
            return None

    def detect_wake_word(self, audio):
        """
        Detect the wake word in audio input.

        Args:
            audio (np.ndarray): Captured audio as a NumPy array.

        Returns:
            bool: True if wake word is detected, False otherwise.
        """
        try:
            if self.vosk_recognizer.AcceptWaveform(audio.tobytes()):
                result = json.loads(self.vosk_recognizer.Result())
                recognized_text = result.get("text", "").lower()
                log(f"Detected text: {recognized_text}", "debug")
                if self.wake_word in recognized_text:
                    log(f"Wake word '{self.wake_word}' detected.", "info")
                    return True
        except Exception as e:
            log(f"Error during wake word detection: {e}", "error")
        return False

    def recognize(self, audio, samplerate=16000):
        """
        Convert speech audio to text using Vosk.

        Args:
            audio (np.ndarray): Captured audio data as a NumPy array.
            samplerate (int): Sampling rate of the captured audio.

        Returns:
            str or None: Recognized text or None if recognition fails.
        """
        if audio is None:
            return None

        try:
            if self.use_vosk:
                log("Using Vosk for offline speech recognition.", "info")
                if self.vosk_recognizer.AcceptWaveform(audio.tobytes()):
                    result = json.loads(self.vosk_recognizer.Result())
                    recognized_text = result.get("text", "")
                    log(f"Recognized text (offline): {recognized_text}", "info")
                    return recognized_text
                else:
                    log("No clear transcription detected.", "warning")
            return None
        except Exception as e:
            log(f"Error during recognition: {e}", "error")
            return None

    def transcribe(self, duration=5):
        """
        High-level method to listen and transcribe speech.

        Args:
            duration (int): Duration in seconds to capture audio.

        Returns:
            str or None: Transcribed text or None if recognition fails.
        """
        audio = self.listen(duration=duration)
        if audio is not None:
            return self.recognize(audio)
        return None

    def set_language(self, vosk_model_path):
        """
        Dynamically change the language by switching the Vosk model.

        Args:
            vosk_model_path (str): Path to the new Vosk language model.

        Returns:
            bool: True if the model was successfully changed, False otherwise.
        """
        if not os.path.exists(vosk_model_path):
            log(f"Language model not found at {vosk_model_path}. Please check the path.", "error")
            return False
        try:
            self.vosk_model = Model(vosk_model_path)
            self.vosk_recognizer = KaldiRecognizer(self.vosk_model, 16000)
            log(f"Language model switched to: {vosk_model_path}", "info")
            return True
        except Exception as e:
            log(f"Error switching language model: {e}", "error")
            return False

    def listen_for_command(self, duration=5):
        """
        Listen for a command after detecting the wake word.

        Args:
            duration (int): Duration to listen for the command.

        Returns:
            str or None: Recognized command text or None if no command is recognized.
        """
        audio = self.listen(duration=duration)
        if audio is not None and len(audio) > 0:  # Explicitly check if audio exists and is not empty
            if self.detect_wake_word(audio):
                log("Wake word detected. Listening for command...", "info")
                return self.transcribe(duration=duration)
        return None


if __name__ == "__main__":
    try:
        stt = SpeechToText(use_vosk=True)
        log("Starting Speech-to-Text module. Say the wake word to activate.", "info")
        while True:
            text = stt.listen_for_command(duration=5)
            if text:
                log(f"You said: {text}", "info")
            else:
                log("No valid command detected.", "warning")
    except KeyboardInterrupt:
        log("Shutting down Speech-to-Text module.", "info")
