from flask import Flask, render_template, redirect, url_for, session
from forms import SearchGame, PickGame, RateGame
from data import search_results

app = Flask(__name__)

app.config["SECRET_KEY"] = "dfewfew123213rwdsgert34tgfd1234trgf"  # A secret key required for the CSRF to work (it's not very secret at the moment)

selected_games = []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    form = SearchGame()
    results = PickGame()
    if form.validate_on_submit():
        matching_games = search_results(form.board_game.data)
        if len(matching_games) > 0:
            print(f"Valid search: {form.board_game.data}")
            return render_template("add.html", form=form, results=results, games=matching_games["name"], amount_added=f"You currently have {len(selected_games)} games added.")
        else:
            form.board_game.errors = [f"{form.board_game.data} could not be found!"]
            print(f"Invalid search: {form.board_game.data}")
    elif results.add_game.data:
        selected_games.append(results.game_name.data)
        print(f"Game added: {results.game_name.data}")
        print(f"Selected games: {selected_games}")
        return redirect(url_for("add"))

    elif form.errors:
        print(form.errors.items())
        print(form.board_game.errors)

    return render_template("add.html", form=form, amount_added=f"You currently have {len(selected_games)} games added.")

@app.route("/rate", methods=["GET", "POST"])
def rate():
    dict_selected_games = [{"game_name": game} for game in selected_games]
    ratings = RateGame(game_ratings=dict_selected_games)
    if ratings.validate_on_submit():
        print(f"Valid Ratings: {ratings.game_ratings.data}")
        print(ratings.game_ratings.data)
        session["ratings"] = ratings.game_ratings.data  # This should be a temporary solution as there is a byte limit on the session data
        return redirect(url_for("analysis"))

    elif ratings.errors:
        print(ratings.errors.items())
        print(ratings.game_ratings.errors)

    return render_template("rate.html", ratings=ratings)

@app.route("/analysis", methods=["GET"])
def analysis():
    ratings_data = session.get("ratings", None)  # Fetches the data from the session
    return render_template("analysis.html", ratings_data=ratings_data)


if __name__ == "__main__":
    app.run(debug=True)