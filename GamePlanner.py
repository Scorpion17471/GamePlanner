from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd

from SteamUserInteraction import get_owned_game_app_ids, get_game_achievement_percentage

def main():
    ID_NAME_LIST = get_owned_game_app_ids(os.getenv("STEAM_API_KEY"), os.getenv("STEAM_USER_ID"))

    for index, (app_id, app_name) in enumerate(ID_NAME_LIST):
        try:
            print(f"{index+1}/{len(ID_NAME_LIST)}: {app_id} - {app_name}...")
            achievement_percentage = get_game_achievement_percentage(os.getenv("STEAM_API_KEY"), os.getenv("STEAM_USER_ID"), app_id)
            with open(f'{os.getenv("STEAM_USER_ID")}.txt', 'a') as f:
                id_name_string = f"{app_id} - {app_name} - "
                achievement_percentage_str = achievement_percentage if type(achievement_percentage) == str else f"{achievement_percentage * 100:.2f}%"

                # GET GAME COMPLETION TIME

                print(id_name_string + achievement_percentage_str, file=f)
        except Exception as e:
            print(f"Error fetching data for app ID {app_id}: {e}")

if __name__ == "__main__":
    load_dotenv()
    main()