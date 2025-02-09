from app.models.game import BoardGame
from flask import current_app

def search_results(user_search):
    with current_app.app_context():
        search_results = BoardGame.query.filter(BoardGame.name.ilike(f"%{user_search}%")).order_by(BoardGame.usersrated.desc()).all()
        return [game.name for game in search_results]

def find_id(game_name):
    game_id = BoardGame.query.filter_by(name=game_name).first()
    return game_id.id

def suitable_games():
    sorted_games = BoardGame.query.order_by(BoardGame.usersrated.desc()).limit(500).all()  # Change the limit to however many games to test for
    return tuple((game.id, game.name) for game in sorted_games)