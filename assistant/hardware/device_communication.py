import socket
import random
from utils.logger import log  # Import the log function

def discover_devices_by_protocol(protocols=["Wi-Fi", "Bluetooth"]):
    """
    Discover devices based on specified protocols (e.g., Wi-Fi, Bluetooth).

    Parameters:
        protocols (list): List of protocols to discover devices by.

    Returns:
        list: List of discovered devices (simulated in this example).
    """
    discovered_devices = []

    # Simulate Wi-Fi device discovery (in real use, replace with actual discovery logic)
    if "Wi-Fi" in protocols:
        # Simulate 3 Wi-Fi devices
        wifi_devices = ["Device-WiFi-1", "Device-WiFi-2", "Device-WiFi-3"]
        discovered_devices.extend(wifi_devices)
        log("Discovered Wi-Fi devices: " + ", ".join(wifi_devices), "info")

    # Simulate Bluetooth device discovery (in real use, replace with actual discovery logic)
    if "Bluetooth" in protocols:
        # Simulate 2 Bluetooth devices
        bluetooth_devices = ["Device-BT-1", "Device-BT-2"]
        discovered_devices.extend(bluetooth_devices)
        log("Discovered Bluetooth devices: " + ", ".join(bluetooth_devices), "info")

    # Add more protocols as needed (e.g., Zigbee, Zigbee, etc.)

    log(f"Total discovered devices: {', '.join(discovered_devices)}", "info")
    return discovered_devices

if __name__ == "__main__":
    discover_devices_by_protocol()