from app.models.game import BoardGame
from flask import current_app

def search_results(user_search):
    with current_app.app_context():
        search_results = BoardGame.query.filter(BoardGame.name.ilike(f"%{user_search}%")).order_by(BoardGame.usersrated.desc()).all()
        return [game.name for game in search_results]

def calculate_weights(ratings):
    weighted_mechanics = {}
    for game in ratings:
        game["mechanics"] = BoardGame.query.filter_by(name=game["game_name"]).first().mechanics
        for mechanic in game["mechanics"]:
            if mechanic not in weighted_mechanics:
                weighted_mechanics[mechanic] = 0
            weighted_mechanics[mechanic] += int(game["rating"])  # int conversion is necessary as the rating is a string
    return weighted_mechanics

def recommend_games(weighted_mechanics, user_games):
    game_scores = []
    games = BoardGame.query.all()
    for game in games:
        if game.name not in user_games and not game.is_expansion:  # Makes sure that the game is not in the user's list and is not an expansion
            total_score = game.bayesaverage * (sum(weighted_mechanics.get(mechanic, 0) for mechanic in game.mechanics))  # Sums all mechanics weights and adds 0 if no weight, then multiplies by the bayesaverage to favour higher rated games
            game_scores.append((game.name, total_score))
    sorted_scores = sorted(game_scores, key=lambda x: x[1], reverse=True)  # Sort by the largest score first
    print(sorted_scores[:10])
    return sorted_scores