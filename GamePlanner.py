from dotenv import load_dotenv
from multiprocessing import Process, Queue
import os
import requests
import json
import pandas as pd
import time
from howlongtobeatpy import HowLongToBeat

from SteamUserInteraction import get_owned_game_app_ids, get_game_achievement_percentage
from HowLongToBeatInteraction import get_game_time

def main():
    ID_NAME_LIST = get_owned_game_app_ids(os.getenv("STEAM_API_KEY"), os.getenv("STEAM_USER_ID"))
    q = Queue()
    hltb = HowLongToBeat(0.7)
    start = time.time()
    for index, (app_id, app_name) in enumerate(ID_NAME_LIST):
        if index > 9:
            break
        try:
            # START TIMER
            
            
            # Start background process to get HLTB time
            c = get_game_time(app_name, q, hltb)
            
            print(f"{index+1}/{len(ID_NAME_LIST)}: {app_id} - {app_name}")
            unlocked_achievements, total_achievements = get_game_achievement_percentage(os.getenv("STEAM_API_KEY"), os.getenv("STEAM_USER_ID"), app_id)
            with open(f'{os.getenv("STEAM_USER_ID")}.txt', 'a') as f:
                id_name_string = f"{app_id} - {app_name} - "
                achievement_percentage_string = f"{unlocked_achievements}" if isinstance(
                    unlocked_achievements, str) else f"{unlocked_achievements}/{total_achievements} Achievements Unlocked"

                # GET GAME COMPLETION TIME
                game_time_string = f" - {c} Hours (Total)"

                print(id_name_string + achievement_percentage_string + game_time_string + f" - {time.time() - start:.3f}s", file=f)
        except Exception as e:
            print(f"Error fetching data for app ID {app_id}: {e}")

if __name__ == "__main__":
    load_dotenv()
    main()