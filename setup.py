import os
import json
import requests
import time

# Constants
API_FILE = "api.json"
RIOT_API_BASE_URL = "https://na1.api.riotgames.com/lol/status/v4/platform-data?api_key="
RETRY_WAIT_TIME = 45  # Seconds to wait before revalidating


# Load the API key from the JSON file
def load_api_key():
    """Loads the API key from the JSON file."""
    if not os.path.exists(API_FILE):
        return None
    with open(API_FILE, "r") as file:
        data = json.load(file)
        return data.get("keyRiot")


# Save the API key to the JSON file
def save_api_key(api_key):
    """Saves the API key to the JSON file."""
    with open(API_FILE, "w") as file:
        json.dump({"keyRiot": api_key}, file, indent=4)


# Validate the API key
def validate_api_key(api_key):
    """Validate the Riot API key by making a request."""
    url = RIOT_API_BASE_URL + api_key
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("API key is valid! Riot API connection successful.")
            return True
        elif response.status_code == 403:
            print("Invalid API key.")
            return False
        else:
            print(f"Unexpected response. Status Code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Riot API: {e}")
        return False


# Prompt the user for a new API key
def prompt_for_api_key():
    """Prompt user to input a new Riot API key."""
    print("Visit https://developer.riotgames.com/ to obtain your API key.")
    while True:
        user_api_key = input("Please enter your Riot API key: ").strip()
        if validate_api_key(user_api_key):
            save_api_key(user_api_key)
            print(f"API key successfully stored in '{API_FILE}'.")
            return user_api_key
        else:
            print("Invalid API key. Please try again.")


# Wait and revalidate the API key before prompting the user
def revalidate_or_prompt(api_key):
    """Wait and revalidate the API key before prompting the user."""
    print(f"API key validation failed. Waiting {RETRY_WAIT_TIME} seconds to try again...")
    time.sleep(RETRY_WAIT_TIME)
    if validate_api_key(api_key):
        print("API key is valid after waiting. No further action needed.")
        return True
    else:
        print("API key is still invalid after waiting.")
        return False


# Main function to check or update the Riot API key
def checkAPI():
    """Main function to check or update the Riot API key."""
    api_key = load_api_key()
    if api_key:
        print("API key found. Validating...")
        if not validate_api_key(api_key):
            if not revalidate_or_prompt(api_key):
                prompt_for_api_key()
    else:
        print("No valid API key found. Prompting for a new one.")
        prompt_for_api_key()
