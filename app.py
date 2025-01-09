from flask import Flask, render_template, redirect, url_for
from forms import SearchGame, PickGame
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
    return render_template("rate.html", selected_games=selected_games)

if __name__ == "__main__":
    app.run(debug=True)