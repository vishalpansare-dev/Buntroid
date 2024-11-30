import threading

from assistant.hardware.device_control import control_device
from assistant.hardware.sensor_control import monitor_sensor, cleanup


def monitor_multiple_sensors():
    """Monitor multiple sensors in parallel."""
    def monitor_temperature():
        monitor_sensor("Temperature", threshold=30, action=lambda: control_device("Fan", "ON"))

    def monitor_humidity():
        monitor_sensor("Humidity", threshold=70, action=lambda: control_device("Dehumidifier", "ON"))

    def monitor_motion():
        monitor_sensor("Motion", action=lambda: control_device("Alarm", "ON"))

    # Start monitoring each sensor in a separate thread
    threading.Thread(target=monitor_temperature, daemon=True).start()
    threading.Thread(target=monitor_humidity, daemon=True).start()
    threading.Thread(target=monitor_motion, daemon=True).start()

if __name__ == "__main__":
    monitor_multiple_sensors()
    cleanup()
