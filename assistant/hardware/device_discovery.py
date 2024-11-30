import serial.tools.list_ports
from utils.logger import log

def discover_devices():
    """Discover all connected devices over serial ports."""
    devices = serial.tools.list_ports.comports()
    if not devices:
        log("No devices found.", "warning")
    for device in devices:
        log(f"Device found: {device.device}, {device.description}", "info")
    return devices

if __name__ == "__main__":
    discover_devices()
