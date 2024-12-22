from setup import checkAPI
from account import getAccount

# Ensure the API key is set up
checkAPI()

# Prompt for player details
gameName = input("Enter the player's game name: ").strip()
tagLine = input("Enter the player's tagline: ").strip()

# Retrieve the player's PUUID and corrected name
puuid = getAccount(gameName, tagLine)
if puuid:
    # Retrieve the corrected name and tagline from accounts.txt
    with open("accounts.txt", "r") as file:
        for line in file:
            if puuid in line:
                corrected_identifier, _ = line.strip().split(" | ")
                print(f"Corrected Player Name: {corrected_identifier}")
                break
    print(f"PUUID: {puuid}")
else:
    print("Failed to retrieve player information.")
