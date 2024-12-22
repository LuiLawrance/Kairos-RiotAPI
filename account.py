import os
import requests

# File to store accounts locally
accounts_file = "accounts.txt"


# Function to retrieve the API key from api.txt
def get_api_key():
    with open("api.txt", "r") as file:
        for line in file:
            if line.startswith("keyRiot"):
                return line.split('=')[1].strip().strip('"')
    raise ValueError("API key not found. Please run setup to initialize it.")


# Function to check if a player exists in accounts.txt
def getAccount(gameName, tagLine):
    """
    Retrieves a player's PUUID based on their gameName and tagLine.
    First checks 'accounts.txt'. If not found, fetches from the Riot API and stores it.
    """
    # Ensure accounts.txt exists
    if not os.path.exists(accounts_file):
        print(f"No '{accounts_file}' file found. Creating one...")
        open(accounts_file, "w").close()

    # Check if player already exists in accounts.txt
    player_identifier_input = f"{gameName}#{tagLine}"
    with open(accounts_file, "r") as file:
        for line in file:
            stored_identifier, puuid = line.strip().split(" | ")
            if stored_identifier.lower() == player_identifier_input.lower():
                print(f"Player '{stored_identifier}' found locally.")
                return puuid

    # If not found, fetch from Riot API
    print(f"Player '{player_identifier_input}' not found locally. Fetching from Riot API...")
    api_key = get_api_key()
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
                with open(accounts_file, "a") as file:
                    file.write(f"{corrected_identifier} | {puuid}\n")
                sortFile()
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


def sortFile():
    """
    Sorts the accounts.txt file alphabetically by gameName.
    """
    if not os.path.exists(accounts_file):
        return

    with open(accounts_file, "r") as file:
        lines = file.readlines()

    # Sort the lines alphabetically based on gameName
    lines.sort(key=lambda line: line.split("#")[0].strip())

    # Write the sorted lines back to the file
    with open(accounts_file, "w") as file:
        file.writelines(lines)
