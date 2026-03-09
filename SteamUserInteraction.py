import requests

def get_owned_game_app_ids(steam_api_key: str, steam_user_id: str):
    """
    Fetches the list of owned game app IDs for a given Steam user.

    Parameters:
    - steam_api_key: Your Steam API key.
    - steam_user_id: The Steam user ID (64-bit) of the user whose owned games you want to fetch.

    Returns:
    - A list of tuples (app ID, game name) representing the games owned by the user.
    """
    STEAM_ENDPOINT_GET_OWNED_GAMES = r"https://api.steampowered.com/"
    STEAM_ENDPOINT_GET_OWNED_GAMES += r"IPlayerService/GetOwnedGames/v0001/?key="
    STEAM_ENDPOINT_GET_OWNED_GAMES += str(steam_api_key) + r"&steamid=" + str(steam_user_id)
    STEAM_ENDPOINT_GET_OWNED_GAMES += r"&include_appinfo=true&include_played_free_games=true"
    
    r = requests.get(STEAM_ENDPOINT_GET_OWNED_GAMES)
    if r.status_code == 200:
        data = r.json()
        ID_NAME_LIST = [(game["appid"], game["name"].encode(encoding='ascii', errors='ignore')
                         .decode('utf-8')) for game in data["response"]["games"]]
        return ID_NAME_LIST
    else:
        raise Exception(f"Failed to fetch owned games: {r.status_code} - {r.text}")

def get_game_achievements(steam_api_key: str, steam_user_id: str, app_id: str):
    """
    Fetches the percentage of achievements unlocked for a specific game for a given Steam user.

    Parameters:
    - steam_api_key: Your Steam API key.
    - steam_user_id: The Steam user ID (64-bit) of the user whose achievements you want to fetch.
    - app_id: The app ID of the game for which you want to fetch achievement data.

    Returns:
    - Tuple containing unlocked and total achievment counts, or (None, None) if the data cannot be fetched
    """
    STEAM_ENDPOINT_GET_ACHIEVEMENTS = r"https://api.steampowered.com/"
    STEAM_ENDPOINT_GET_ACHIEVEMENTS += r"ISteamUserStats/GetPlayerAchievements/v0001/?key="
    STEAM_ENDPOINT_GET_ACHIEVEMENTS += str(steam_api_key) + "&steamid=" + str(steam_user_id)
    STEAM_ENDPOINT_GET_ACHIEVEMENTS += "&appid=" + str(app_id)
    
    r = requests.get(STEAM_ENDPOINT_GET_ACHIEVEMENTS)
    if r.status_code == 200:
        data = r.json()
        if "playerstats" in data and "achievements" in data["playerstats"]:
            achievements = data["playerstats"]["achievements"]
            unlocked_count = sum(1 for ach in achievements if ach["achieved"] == 1)
            return (unlocked_count, len(achievements))
        return (None, None)
    else:
        return (None, None)