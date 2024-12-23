from setup import checkAPI
from account import getAccount

# Ensure the API key is set up
checkAPI()

current_mode = None

while True:
    # Check if the user needs to select a mode
    if current_mode is None:
        print("------------------------------")
        mode = input(
            "Select a mode:\n1. Riot Player Search\n\nType 'exit' to end the script.\nYour choice: ").strip().lower()
        print("------------------------------")

        if mode == '1':
            current_mode = '1'
        elif mode == 'exit':
            print("Exiting the script. Goodbye!")
            print("------------------------------")
            break
        else:
            print("Invalid choice. Please select '1' or type 'exit'.")
            continue

    # Handle Riot Player Search mode
    if current_mode == '1':
        print("Riot Player Search Mode (type 'E#E' as the player name to return to the main menu).")
        print()

        # Prompt for player details
        gameName = input("Enter the player's game name (or 'gameName#tagLine'): ").strip()

        # Check if the user wants to return to the main menu
        if gameName.upper() == "E#E":
            current_mode = None
            continue

        # Check if the input contains a #
        if '#' in gameName:
            gameName, tagLine = gameName.split('#', 1)
        else:
            tagLine = input("Enter the player's tagline: ").strip()

        print("------------------------------")
        puuid = getAccount(gameName, tagLine)

        # Check if the PUUID was successfully retrieved
        if puuid:
            print(f"PUUID: {puuid}")
        else:
            print("Failed to retrieve player information. Please check the game name and tagline.")
