from flask import Flask, render_template, request
from forms import BoardGameForm
from data import find_game

app = Flask(__name__)

app.config["SECRET_KEY"] = "dfewfew123213rwdsgert34tgfd1234trgf"  # A secret key required for the CSRF to work (it's not very secret at the moment)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    form = BoardGameForm()
    if form.validate_on_submit():
        if find_game(form.board_game.data):
            print(f"Valid Board Game: {form.board_game.data}")
            return render_template("lookup.html", form=form, message=f"{form.board_game.data} successfully found!")
        else:
            print(f"Invalid Board Game: {form.board_game.data}")
            return render_template("lookup.html", form=form, message=f"{form.board_game.data} could not be found!")
    elif form.errors:
        print(form.errors.items())
        print(form.board_game.errors)
    return render_template("lookup.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)