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

def game_details(game_id):
    game = BoardGame.query.filter_by(id=game_id).first()
    return game.mechanics

def recommend_games(weighted_mechanics, user_games):
    game_scores = []
    games = BoardGame.query.all()
    for game in games:
        if game.name not in user_games:
            total_score = sum(weighted_mechanics.get(mechanic, 0) for mechanic in game.mechanics)  # Sums all mechanics weights and adds 0 if no weight
            game_scores.append((game.name, total_score))
    sorted_scores = sorted(game_scores, key=lambda x: x[1], reverse=True)  # Sort by the largest score first
    print(sorted_scores[:10])
    return sorted_scores