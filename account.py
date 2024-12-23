import os
import json
import requests

# File to store accounts locally
accounts_file = "accounts.json"
api_file = "api.json"


# Load the API key from the JSON file
def get_api_key():
    """Loads the API key from the JSON file."""
    if not os.path.exists(api_file):
        raise ValueError(f"{api_file} not found. Please run setup to initialize the API key.")
    with open(api_file, "r") as file:
        data = json.load(file)
        api_key = data.get("keyRiot")
        if not api_key:
            raise ValueError(f"API key not found in {api_file}. Please run setup to configure it.")
        return api_key


# Load accounts from the JSON file
def load_accounts():
    """Loads accounts from the JSON file."""
    if not os.path.exists(accounts_file):
        return {}
    with open(accounts_file, "r") as file:
        return json.load(file)


# Save accounts to the JSON file
def save_accounts(accounts):
    """Saves accounts to the JSON file."""
    with open(accounts_file, "w") as file:
        json.dump(accounts, file, indent=4)


# Function to check if a player exists in accounts.json
def getAccount(gameName, tagLine):
    """
    Retrieves a player's PUUID based on their gameName and tagLine.
    First checks 'accounts.json'. If not found, fetches from the Riot API and stores it.
    If a matching PUUID is found but the locally stored name is incorrect, updates the local entry.
    """
    # Load existing accounts
    accounts = load_accounts()
    player_identifier_input = f"{gameName}#{tagLine}"
    api_key = get_api_key()

    # Normalize input to ensure case-insensitive comparison
    player_identifier_input_lower = player_identifier_input.lower()

    # Check if the PUUID already exists locally
    for puuid, account in accounts.items():
        stored_identifier = f"{account['gameName']}#{account['tagLine']}"
        stored_identifier_lower = stored_identifier.lower()

        # If the player identifier matches, return the PUUID
        if stored_identifier_lower == player_identifier_input_lower:
            print(f"Player '{stored_identifier}' found locally.")
            return puuid

        # If the PUUID matches, verify and update the name if necessary
        if puuid == account.get("puuid"):
            print(f"PUUID match found for '{stored_identifier}'. Verifying name...")
            url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                corrected_gameName = data.get("gameName")
                corrected_tagLine = data.get("tagLine")
                corrected_identifier = f"{corrected_gameName}#{corrected_tagLine}"

                # Update the name if it's incorrect
                if corrected_identifier.lower() != stored_identifier_lower:
                    print(f"Updating name in accounts.json: '{stored_identifier}' -> '{corrected_identifier}'.")
                    accounts[puuid] = {"gameName": corrected_gameName, "tagLine": corrected_tagLine}
                    save_accounts(accounts)
                return puuid

    # If not found, fetch from Riot API
    print(f"Player '{player_identifier_input}' not found locally. Fetching from Riot API...")
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            puuid = data.get("puuid")
            corrected_gameName = data.get("gameName")
            corrected_tagLine = data.get("tagLine")

            if puuid:
                # Store returned player info locally
                corrected_identifier = f"{corrected_gameName}#{corrected_tagLine}"
                accounts[puuid] = {"gameName": corrected_gameName, "tagLine": corrected_tagLine}
                save_accounts(accounts)
                print(f"Player '{corrected_identifier}' stored locally with PUUID.")
                return puuid
        elif response.status_code == 403:
            print("Invalid API key. Please reconfigure it using setup.py.")
        elif response.status_code == 404:
            print(f"Player '{player_identifier_input}' not found in Riot API.")
        else:
            print(f"Failed to fetch player data. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to Riot API: {e}")

    return None
