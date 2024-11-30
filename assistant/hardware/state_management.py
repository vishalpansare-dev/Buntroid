from utils.logger import log

device_state = {}

def set_device_state(device, state):
    """Set the state of a device."""
    device_state[device] = state
    log(f"Device {device} set to {state}.", "info")

def get_device_state(device):
    """Get the current state of a device."""
    state = device_state.get(device, "Unknown")
    log(f"Device {device} state: {state}", "info")
    return state
