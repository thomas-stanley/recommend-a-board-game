import pandas as pd

def search_results(user_search):
    board_game_df = pd.read_csv("data/boardgames_ranks.csv")
    search_results = board_game_df[board_game_df["name"].str.contains(user_search, case=False)]
    return search_results.sort_values(by="usersrated", ascending=False)

def find_id(game_name):
    board_game_df = pd.read_csv("data/boardgames_ranks.csv")
    game_id = board_game_df[board_game_df["name"] == game_name]["id"]
    return game_id.iloc[0]

def suitable_games():
    board_game_df = pd.read_csv("data/boardgames_ranks.csv")
    sorted_games = board_game_df.sort_values(by="usersrated", ascending=False).head(40) # Change head to however many games you want to test
    return sorted_games[["name", "id"]] 

def main():
    print(search_results("Pandemic"))
    print(find_id("Pandemic"))

if __name__ == "__main__":
    main()