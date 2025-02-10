from flask import Blueprint, render_template, redirect, url_for, session
from app.forms import SearchGame, PickGame, RateGame
from app.handle_db import search_results, game_details, recommend_games
board_games = Blueprint("board_games", __name__)


@board_games.route("/")
def home():
    if "selected_games" not in session:  # It may be worth removing this so that the user can start again selecting games if they wish
        session["selected_games"] = []
    return render_template("home.html")

@board_games.route("/add", methods=["GET", "POST"])
def add():
    form = SearchGame()
    results = PickGame()
    if form.validate_on_submit():
        matching_games = search_results(form.board_game.data)
        print(matching_games[:5])  # Only print the first 5 matching games
        if len(matching_games) > 0:
            print(f"Valid search: {form.board_game.data}")
            return render_template("add.html", form=form, results=results, games=matching_games, amount_added=f"You currently have {len(session["selected_games"])} games added.")
        else:
            form.board_game.errors = [f"{form.board_game.data} could not be found!"]
            print(f"Invalid search: {form.board_game.data}")

    elif results.add_game.data:
        session["selected_games"].append(results.game_name.data)
        session.modified = True  # Mutable data structure so the session needs to know an update has occurred
        print(f"Game added: {results.game_name.data}")
        print(f"Selected games: {session["selected_games"]}")
        return redirect(url_for("board_games.add"))

    elif form.errors:
        print(form.errors.items())
        print(form.board_game.errors)

    return render_template("add.html", form=form, amount_added=f"You currently have {len(session["selected_games"])} games added.")

@board_games.route("/rate", methods=["GET", "POST"])
def rate():
    dict_selected_games = tuple({"game_name": game} for game in session["selected_games"])  # Data won't be altered to tuple is better than a list
    ratings = RateGame(game_ratings=dict_selected_games)
    if ratings.validate_on_submit():
        print(f"Valid Ratings: {tuple(game["game_name"] for game in ratings.game_ratings.data)}")
        session["ratings"] = ratings.game_ratings.data
        return redirect(url_for("board_games.analysis"))

    elif ratings.errors:
        print(ratings.errors.items())
        print(ratings.game_ratings.errors)

    return render_template("rate.html", ratings=ratings)

@board_games.route("/analysis", methods=["GET"])
def analysis():
    ratings_data = session["ratings"]  # Fetches the data from the session; ratings_data holds game_name, rating, csrf_token
    weighted_mechanics = {}
    for game in ratings_data:
        game["mechanics"] = game_details(game["game_name"])
        for mechanic in game["mechanics"]:
            if mechanic not in weighted_mechanics:
                weighted_mechanics[mechanic] = 0
            weighted_mechanics[mechanic] += int(game["rating"])
    user_games = [game["game_name"] for game in ratings_data]
    recommended_games = recommend_games(weighted_mechanics, user_games)[:5]  # First 5 elements of the recommended games
    return render_template("analysis.html", recommended_games=recommended_games)
