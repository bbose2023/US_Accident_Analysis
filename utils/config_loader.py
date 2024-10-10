import json
import sys


def load_config(config_file):
    """Function to load configuration from a JSON file"""
    try:
        # Open and read the configuration file with UTF-8 encoding
        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        # Handle the case where the configuration file is not found
        print(f"Configuration file {config_file} not found.")
        sys.exit()
    except json.JSONDecodeError:
        # Handle JSON decoding errors
        print(f"Error decoding JSON from the configuration file {config_file}.")
        sys.exit()