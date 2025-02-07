from app.models.game import BoardGame
from flask import current_app

def search_results(user_search):
    with current_app.app_context():
        search_results = BoardGame.query.filter(BoardGame.name.ilike(f"%{user_search}%")).order_by(BoardGame.usersrated.desc()).all()
        return [game.name for game in search_results]

"""
def find_id(game_name):
    board_game_df = pd.read_csv("data/boardgames_ranks.csv")
    game_id = board_game_df[board_game_df["name"] == game_name]["id"]
    return game_id.iloc[0]

def suitable_games():
    board_game_df = pd.read_csv("data/boardgames_ranks.csv")
    sorted_games = board_game_df.sort_values(by="usersrated", ascending=False).head(500) # Change head to however many games you want to test
    return sorted_games[["name", "id"]] 
"""