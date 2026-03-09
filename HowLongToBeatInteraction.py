def get_game_time(game_name: str, HLTB):
    """
    Fetches the estimated completion time for a given game from HowLongToBeat.

    Parameters:
    - game_name: The name of the game for which to fetch the completion time.
    - HLTB: HowLongToBeat instance to use for searching the game.

    Returns:
    - None | Exception: The function does not return a value but
        puts the estimated completion time in the provided queue.
        If an error occurs, it prints the error message.
    """
    try:
        results = HLTB.search(game_name, similarity_case_sensitive=False)
        if results is not None and len(results) > 0:
            best_element = max(results, key=lambda element: element.similarity)
            
            # Get longest time for game entry
            return max(
                best_element.main_story,
                best_element.main_extra,
                best_element.completionist,
                best_element.all_styles,
                best_element.coop_time,
                best_element.mp_time
            )
    except Exception as e:
        return None