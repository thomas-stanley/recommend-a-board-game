from flask import Flask, render_template, request
from forms import BoardGameForm
from data import find_game, search_results

app = Flask(__name__)

app.config["SECRET_KEY"] = "dfewfew123213rwdsgert34tgfd1234trgf"  # A secret key required for the CSRF to work (it's not very secret at the moment)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    form = BoardGameForm()
    if form.validate_on_submit():
        matching_games = search_results(form.board_game.data)
        if len(matching_games) > 0:
            print(f"Valid search: {form.board_game.data}")
            return render_template("add.html", form=form, games=matching_games["name"])
        else:
            form.board_game.errors = [f"{form.board_game.data} could not be found!"]
            print(f"Invalid search: {form.board_game.data}")

    elif form.errors:
        print(form.errors.items())
        print(form.board_game.errors)

    return render_template("add.html", form=form)

@app.route("/rate", methods=["GET", "POST"])
def rate():
    return render_template("rate.html")

if __name__ == "__main__":
    app.run(debug=True)