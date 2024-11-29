from speech_recognitions import initialize_recognition, recognize_speech, stop_recognition
from text_to_speech import initialize_speech_engine, speak
from task_manager import add_task, list_tasks, delete_task


def main():
    """Main function to run the assistant."""
    # Initialize Speech Recognition and Text-to-Speech
    recognizer = initialize_recognition("/Users/vishal_pansare/PycharmProjects/Buntroid/models/vosk-model")
    engine = initialize_speech_engine()

    # Greet the user
    speak(engine, "Hello, how can I assist you today?")

    try:
        while True:
            # Listen for speech input
            recognized_text = recognize_speech(recognizer)
            if recognized_text:
                print(f"Recognized: {recognized_text}")
                speak(engine, f"You said: {recognized_text}")

                # Task-related commands
                if "hello" in recognized_text.lower():
                    task_name = recognized_text.lower().replace("hello", "").strip()
                    if task_name:
                        add_task(task_name)
                        speak(engine, f"Task '{task_name}' added.")
                    else:
                        speak(engine, "Please provide a task name.")

                elif "list tasks" in recognized_text.lower():
                    tasks = list_tasks()
                    speak(engine, f"Your tasks are: {tasks}")

                elif "delete task" in recognized_text.lower():
                    try:
                        task_number = int(recognized_text.split("task")[-1].strip())
                        result = delete_task(task_number - 1)  # Convert to zero-based index
                        speak(engine, result)
                    except ValueError:
                        speak(engine, "Please specify the task number to delete.")

                elif "stop" in recognized_text.lower():
                    speak(engine, "Goodbye!")
                    break

    except KeyboardInterrupt:
        pass
    finally:
        # Stop recognition and cleanup
        stop_recognition()
        print("Assistant stopped.")


if __name__ == "__main__":
    main()
