from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat
import os
import pandas as pd
import time

from SteamUserInteraction import get_owned_game_app_ids, get_game_achievements
from HowLongToBeatInteraction import get_game_time

def main():
    ID_NAME_LIST = get_owned_game_app_ids(os.getenv("STEAM_API_KEY"), os.getenv("STEAM_USER_ID"))
    HLTB = HowLongToBeat(0.7)
    df = pd.DataFrame({
        "Steam App ID": [],
        "Game Name": [],
        "Unlocked Achievements": [],
        "Total Achievements": [],
        "Estimated 100% Time (hrs)": []
    })
    START_TIME = time.time()
    for index, (app_id, app_name) in enumerate(ID_NAME_LIST):
        try:
            # Print progress
            print(f"{index+1}/{len(ID_NAME_LIST)}: {app_id} - {app_name} - {time.time() - START_TIME:.2f}s elapsed...")

            # Fetch achievement/time data
            unlocked_achievements, total_achievements = get_game_achievements(os.getenv("STEAM_API_KEY"), os.getenv("STEAM_USER_ID"), app_id)
            game_time = get_game_time(app_name, HLTB)

            # Record data
            df.loc[len(df)] = [app_id, app_name, unlocked_achievements, total_achievements, game_time]
        except Exception as e:
            print(f"Error fetching data for app ID {app_id}: {e}")
    df.to_csv(f"{os.getenv("STEAM_USER_ID")}_formatted.csv", index=False)

if __name__ == "__main__":
    load_dotenv()
    main()