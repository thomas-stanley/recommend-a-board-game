import pandas as pd

def search_results(user_search):
    board_game_df = pd.read_csv("boardgames_ranks.csv")
    search_results = board_game_df[board_game_df["name"].str.contains(user_search, case=False)]
    return search_results.sort_values(by="usersrated", ascending=False)

def main():
    print(search_results("Pandemic"))

if __name__ == "__main__":
    main()