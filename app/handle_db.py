from app.models.game import BoardGame
from flask import current_app

def search_results(user_search):
    with current_app.app_context():
        search_results = BoardGame.query.filter(BoardGame.name.ilike(f"%{user_search}%")).order_by(BoardGame.usersrated.desc()).all()
        return [game.name for game in search_results]

def calculate_weights(ratings):
    weighted_features = {}
    for game in ratings:
        game["features"] = BoardGame.query.filter_by(name=game["game_name"]).first().features
        for feature in game["features"]:
            if feature not in weighted_features:
                weighted_features[feature] = 0
            weighted_features[feature] += int(game["rating"])  # int conversion is necessary as the rating is a string
    return weighted_features

def recommend_games(weighted_features, user_games):
    game_scores = []
    games = BoardGame.query.all()
    for game in games:
        if game.name not in user_games and not game.is_expansion:  # Makes sure that the game is not in the user's list and is not an expansion
            total_score = game.bayesaverage * (sum(weighted_features.get(feature, 0) for feature in game.features))  # Sums all features weights and adds 0 if no weight, then multiplies by the bayesaverage to favour higher rated games
            game_scores.append((game.name, total_score))
    sorted_scores = sorted(game_scores, key=lambda x: x[1], reverse=True)  # Sort by the largest score first
    print(sorted_scores[:10])
    return sorted_scores