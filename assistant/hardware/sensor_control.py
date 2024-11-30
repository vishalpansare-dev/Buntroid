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
    exit(1)

# Read sensor data from Arduino
def read_sensor_data(sensor):
    """Read data from a specific sensor (e.g., temperature, motion, humidity, light)."""
    try:
        arduino.write(f"READ_{sensor}".encode())  # Send command to Arduino to read sensor
        sensor_data = arduino.readline().decode().strip()  # Read sensor data
        log(f"Sensor {sensor} data: {sensor_data}", "info")
        return sensor_data
    except Exception as e:
        log(f"Error reading sensor data: {e}", "error")
        return None

def monitor_sensor(sensor, threshold=None, action=None):
    """Monitor a sensor continuously, trigger action if threshold is met."""
    while True:
        sensor_data = read_sensor_data(sensor)
        if sensor_data is not None:
            # Check threshold and trigger action if necessary
            try:
                if threshold and float(sensor_data) > threshold:
                    log(f"Threshold exceeded for {sensor}: {sensor_data}", "warning")
                    if action:
                        action()  # Perform a specific action (e.g., turn on device)
            except ValueError:
                log(f"Invalid sensor data received for {sensor}: {sensor_data}", "error")
        time.sleep(1)

def cleanup():
    """Close the serial connection."""
    if arduino.is_open:
        arduino.close()
        log("Serial connection closed.", "info")

if __name__ == "__main__":
    # Example: Monitor temperature sensor and trigger action if temperature exceeds 30°C
    def turn_on_fan():
        control_device("Fan", "ON")

    monitor_sensor("Temperature", threshold=30, action=turn_on_fan)
    monitor_sensor("Humidity", threshold=70, action=lambda: control_device("Dehumidifier", "ON"))
    cleanup()
