import re
from utils.logger import log
from assistant.nlp.text_processing import clean_text
from assistant.hardware.device_discovery import discover_devices
from assistant.hardware.device_control import control_device
from assistant.media.media_player import MediaPlayer
from assistant.automation.custom_scripts import list_available_scripts, run_single_script
from assistant.hardware.device_communication import discover_devices_by_protocol  # Import extended device discovery

# Enhanced intent classification based on various project tasks
intents = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "goodbye": ["goodbye", "bye", "see you", "take care"],
    "task": ["create", "schedule", "set up", "run", "execute", "activate", "deactivate"],
    "device_control": ["turn on", "turn off", "activate", "deactivate", "switch", "control"],
    "media_control": ["play", "pause", "stop", "next", "previous", "volume", "mute"],
    "hardware_status": ["status", "check", "report", "state", "is it working", "active", "inactive"],
    "automation_control": ["start", "stop", "pause", "resume", "schedule", "execute script"],
    "information": ["what", "who", "how", "where", "why"]
}

# Store recently interacted devices, tasks, and user preferences for context management
user_context = {
    "last_device": None,
    "last_task": None,
    "preferred_volume": 50,  # Default volume
    "frequent_devices": [],  # Track devices frequently interacted with
    "time_of_day": None  # Track the time of day for personalized greetings
}


def classify_query(query):
    """
    Classifies the user's query into predefined intents.
    """
    query = clean_text(query)  # Clean the query for uniformity
    words = query.split()

    for intent, keywords in intents.items():
        if any(word in words for word in keywords):
            return intent
    return "unknown"


def handle_task(query):
    """
    Handle task-related queries such as creating or scheduling tasks.
    """
    available_scripts = list_available_scripts()  # Get available scripts dynamically
    if "create" in query or "schedule" in query:
        return "What task would you like to create or schedule?"
    elif "run" in query or "execute" in query:
        task = extract_task(query, available_scripts)
        if task:
            run_single_script(task)
            user_context["last_task"] = task  # Update context with the last task run
            return f"Running task: {task}"
    return "I couldn't understand the task. Could you clarify?"


def handle_device_control(query):
    """
    Handle queries related to device control like turning on/off devices.
    """
    # Discover devices by different protocols (e.g., Wi-Fi, Bluetooth, etc.)
    available_devices = discover_devices_by_protocol(["Wi-Fi", "Bluetooth"])  # Dynamic discovery based on protocols
    if "turn on" in query or "activate" in query:
        device = extract_device(query, available_devices)
        if device:
            control_device(device, "on")
            user_context["last_device"] = device  # Update context with the last device controlled
            update_frequent_devices(device)  # Track frequent devices
            return f"{device} has been turned on."
        return "Which device would you like to activate?"
    elif "turn off" in query or "deactivate" in query:
        device = extract_device(query, available_devices)
        if device:
            control_device(device, "off")
            user_context["last_device"] = device  # Update context with the last device controlled
            update_frequent_devices(device)  # Track frequent devices
            return f"{device} has been turned off."
    return "I couldn't control the device. Could you specify the device?"


def handle_media_control(query):
    """
    Handle queries related to controlling media playback.
    """
    player = MediaPlayer()

    if "play" in query:
        player.play_media("sample.mp3")  # Placeholder media file
        return "Now playing your media."
    elif "pause" in query:
        player.pause_media()
        return "Media paused."
    elif "stop" in query:
        player.stop_media()
        return "Media stopped."
    elif "next" in query:
        player.next_media()
        return "Playing next media."
    elif "previous" in query:
        player.previous_media()
        return "Playing previous media."
    elif "volume" in query:
        volume_level = extract_volume(query)
        if volume_level:
            player.set_volume(volume_level)
            user_context["preferred_volume"] = volume_level  # Save the preferred volume
            return f"Volume set to {volume_level}."
    elif "mute" in query:
        player.mute_media()
        return "Media muted."
    return "I couldn't understand the media control command."


def handle_hardware_status(query):
    """
    Handle queries asking for the status of hardware devices.
    """
    # Check the status of a device (for simplicity, just an example device check)
    if "is it working" in query:
        device = extract_device(query)
        if device:
            # Check the status of the device
            status = "active"  # Placeholder for actual device status
            return f"{device} is currently {status}."
    return "I couldn't find any device status information."


def handle_automation_control(query):
    """
    Handle queries related to controlling or running automation tasks.
    """
    if "start" in query or "run" in query:
        task = extract_task(query)
        if task:
            run_single_script(task)
            user_context["last_task"] = task  # Update context with the last task run
            return f"Running task: {task}"
    elif "stop" in query or "pause" in query:
        # Implement logic for stopping or pausing tasks
        return "Automation task has been paused or stopped."
    return "I couldn't manage the automation. Could you clarify?"


def extract_device(query, available_devices):
    """
    Extracts the device name from the query based on the dynamically discovered devices.
    """
    for device in available_devices:
        if device.lower() in query.lower():
            return device
    return user_context["last_device"] if user_context["last_device"] else None


def extract_task(query, available_scripts):
    """
    Extract task name from the query based on available tasks.
    """
    for task in available_scripts:
        if task.lower() in query.lower():
            return task
    return user_context["last_task"] if user_context["last_task"] else None


def extract_volume(query):
    """
    Extract volume level from the query.
    """
    volume_levels = ["low", "medium", "high", "mute"]
    for level in volume_levels:
        if level in query:
            if level == "mute":
                return 0
            return 50 if level == "medium" else 100 if level == "high" else 10
    return None


def update_frequent_devices(device):
    """
    Track and update the list of frequently controlled devices.
    """
    if device not in user_context["frequent_devices"]:
        user_context["frequent_devices"].append(device)
    if len(user_context["frequent_devices"]) > 5:
        user_context["frequent_devices"].pop(0)  # Limit the list to the last 5 devices


def handle_query(query):
    """
    Handles the query by classifying it and mapping to a task.
    """
    intent = classify_query(query)

    if intent == "greeting":
        # Personalized greeting based on time of day
        if user_context["time_of_day"]:
            return f"Good {user_context['time_of_day']}! How can I assist you today?"
        return "Hello! How can I assist you today?"

    elif intent == "goodbye":
        return "Goodbye! Have a great day!"
    elif intent == "task":
        return handle_task(query)
    elif intent == "device_control":
        return handle_device_control(query)
    elif intent == "media_control":
        return handle_media_control(query)
    elif intent == "hardware_status":
        return handle_hardware_status(query)
    elif intent == "automation_control":
        return handle_automation_control(query)
    elif intent == "information":
        return "I can help you with a variety of tasks, just ask!"
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"


# Test the enhanced query understanding
if __name__ == "__main__":
    test_query = "Can you play some music?"
    print("Response:", handle_query(test_query))
