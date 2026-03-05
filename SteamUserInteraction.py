import requests

def get_owned_game_app_ids(steam_api_key, steam_user_id):
    """
    Fetches the list of owned game app IDs for a given Steam user.

    Parameters:
    - steam_api_key: Your Steam API key.
    - steam_user_id: The Steam user ID (64-bit) of the user whose owned games you want to fetch.

    Returns:
    - A list of app IDs representing the games owned by the user.
    """
    STEAM_ENDPOINT_GET_OWNED_GAMES = r"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
    STEAM_ENDPOINT_GET_OWNED_GAMES += steam_api_key + "&steamid=" + steam_user_id + "&include_appinfo=true&include_played_free_games=true"
    
    r = requests.get(STEAM_ENDPOINT_GET_OWNED_GAMES)
    if r.status_code == 200:
        data = r.json()
        ID_NAME_LIST = [(game["appid"], game["name"].encode(encoding='ascii', errors='ignore').decode('ascii')) for game in data["response"]["games"]]
        return ID_NAME_LIST
    else:
        raise Exception(f"Failed to fetch owned games: {r.status_code} - {r.text}")

def get_game_achievement_percentage(steam_api_key, steam_user_id, app_id):
    """
    Fetches the percentage of achievements unlocked for a specific game for a given Steam user.

    Parameters:
    - (str) steam_api_key: Your Steam API key.
    - (str) steam_user_id: The Steam user ID (64-bit) of the user whose achievements you want to fetch.
    - (int | str) app_id: The app ID of the game for which you want to fetch achievement data.

    Returns:
    - (float) The percentage of achievements unlocked for that game.
    """
    STEAM_ENDPOINT_GET_ACHIEVEMENTS = r"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?key="
    STEAM_ENDPOINT_GET_ACHIEVEMENTS += steam_api_key + "&steamid=" + steam_user_id + "&appid=" + str(app_id)
    
    r = requests.get(STEAM_ENDPOINT_GET_ACHIEVEMENTS)
    if r.status_code == 200:
        data = r.json()
        achievement_percent = 0.0
        if "playerstats" in data and "achievements" in data["playerstats"]:
            achievements = data["playerstats"]["achievements"]
            achievement_percent = sum(1 for ach in achievements if ach["achieved"] == 1) / len(achievements)
        return achievement_percent
    else:
        return "N/A"