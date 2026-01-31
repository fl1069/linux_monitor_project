import json
import os

# Default configuration
DEFAULT_CONFIG = {
    "monitor_dir": "test_folder",          # Directory to monitor
    "log_dir": "logs",                     # Log storage directory
    "check_interval": 2,                   # Check interval (seconds)
    "watch_events": ["create", "delete", "modify"],  # Events to monitor
    "log_file": "directory_changes.log"    # Log file name
}

def load_config(config_file="config.json"):
    """Load configuration from file"""
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except:
            print(f"⚠️  Configuration file {config_file} is corrupted, using default configuration")
    else:
        print(f"⚠️  Configuration file {config_file} not found, using default configuration")

    return DEFAULT_CONFIG

def save_config(config, config_file="config.json"):
    """Save configuration to file"""
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)
    print(f"✅ Configuration saved to {config_file}")

def print_config(config):
    """Print current configuration"""
    print("\nCurrent Configuration:")
    print("-" * 30)
    for key, value in config.items():
        print(f"{key:15}: {value}")

def setup_config():
    """Initialize configuration file"""
    if not os.path.exists("config.json"):
        save_config(DEFAULT_CONFIG)
        print("✅ Default configuration file config.json created")
    return load_config()

# Test
if __name__ == "__main__":
    print("Testing configuration file...")

    # Load configuration
    config = setup_config()

    # Display configuration
    print_config(config)

    # Modify and save configuration
    config["monitor_dir"] = "my_monitor_folder"
    save_config(config)
