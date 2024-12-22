import os
import requests

def checkAPI():
    file_name = "api.txt"

    # Function to validate the format 'keyRiot = "value"'
    def is_valid_key(line):
        return line.startswith('keyRiot = "') and line.endswith('"\n"')

    # Function to extract Riot API key from file
    def extract_api_key():
        with open(file_name, "r") as file:
            for line in file:
                if is_valid_key(line):
                    return line.split('=')[1].strip().strip('"')
        return None

    # Function to validate API key
    def validate_api_key(api_key):
        url = f"https://na1.api.riotgames.com/lol/status/v4/platform-data?api_key={api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("API key is valid! Riot API connection successful.")
                return True
            elif response.status_code == 403:
                print("Invalid API key. Please provide a new one.")
                return False
            else:
                print(f"Failed to validate API key. Status Code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error connecting to Riot API: {e}")
            return False

    # Function to prompt user for a new API key
    def prompt_for_api_key():
        print("Go to this link to obtain your API key: https://developer.riotgames.com/")
        while True:
            user_api_key = input("Please enter your Riot API key: ").strip()
            if validate_api_key(user_api_key):
                with open(file_name, "w") as file:
                    file.write(f'keyRiot = "{user_api_key}"\n')
                print(f"API key successfully stored in '{file_name}' as 'keyRiot'.")
                return user_api_key
            else:
                print("Invalid API key. Please try again.")

    # Check if 'api.txt' exists
    if not os.path.exists(file_name):
        print("No 'api.txt' file found. Creating one now...")
        prompt_for_api_key()
    else:
        print(f"'{file_name}' found. Checking content...")
        api_key = extract_api_key()
        if api_key:
            print("Found API key in file. Validating...")
            if not validate_api_key(api_key):
                prompt_for_api_key()
        else:
            print("No valid API key found in the file.")
            prompt_for_api_key()
