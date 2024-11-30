from assistant.speech.speech_to_text import SpeechToText
from assistant.nlp.query_understanding import QueryUnderstanding
from utils.logger import log


if __name__ == "__main__":
    try:
        # Initialize speech recognition and NLP
        stt = SpeechToText(use_vosk=True, vosk_model_path="models/vosk-model-en-in-0.5")
        assistant = QueryUnderstanding()

        log("Assistant is active. Say 'Hey Assistant' to activate.", "info")
        while True:
            command = stt.listen_for_command(duration=5)
            if command:
                response = assistant.process_command(command)
                log(response, "info")
    except KeyboardInterrupt:
        log("Shutting down assistant.", "info")
    except Exception as e:
        log(f"An unexpected error occurred: {e}", "error")
