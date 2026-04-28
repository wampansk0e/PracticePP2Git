import json
import os

SETTINGS_FILE = "settings.json"

# Default preferences
DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0], # Green
    "grid_overlay": True,
    "sound": True
}

def load_settings():
    """Loads preferences from local JSON file on startup."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS

def save_settings(settings_dict):
    """Saves preferences when changed in the Settings screen."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings_dict, f, indent=4)