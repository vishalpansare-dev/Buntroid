import serial
import time
from utils.logger import log

# Set up the serial connection to Arduino
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust based on your system
BAUD_RATE = 9600

# Establish serial connection
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
    log(f"Connected to Arduino on {SERIAL_PORT}", "info")
except serial.SerialException as e:
    log(f"Error connecting to Arduino: {e}", "error")
    # exit(1)

# Send command to Arduino
def send_command_to_device(command):
    """Send command to the Arduino to control a device (LED, motor, etc.)."""
    try:
        arduino.write(command.encode())
        log(f"Command sent to Arduino: {command}", "info")
    except Exception as e:
        log(f"Error sending command: {e}", "error")

# Example function to turn on/off a device (LED, motor, relay)
def control_device(device, state):
    """Control a device on/off."""
    command = f"{device}:{state}"
    send_command_to_device(command)

def get_device_state(device):
    """Get the current state of a device."""
    try:
        arduino.write(f"GET_STATE_{device}".encode())
        state = arduino.readline().decode().strip()
        log(f"Device {device} state: {state}", "info")
        return state
    except Exception as e:
        log(f"Error getting device state: {e}", "error")
        return "Unknown"

def cleanup():
    """Close the serial connection."""
    if arduino.is_open:
        arduino.close()
        log("Serial connection closed.", "info")

if __name__ == "__main__":
    control_device("LED", "ON")
    time.sleep(2)  # Keep the LED on for 2 seconds
    control_device("LED", "OFF")
    control_device("Motor", "ON")
    time.sleep(2)
    control_device("Motor", "OFF")
    cleanup()
