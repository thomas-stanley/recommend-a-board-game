import pandas as pd

def find_game(game_name):  # Currently the search is case-sensitive which needs to be fixed
    board_game_df = pd.read_csv("boardgames_ranks.csv")
    game_present = (board_game_df["name"] == game_name).any()
    return game_present