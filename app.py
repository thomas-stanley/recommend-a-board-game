from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    if request.method == "POST":
        board_game = request.form["board_game"]
        return render_template("lookup.html", message=f"You searched for {board_game}.")
    return render_template("lookup.html")


if __name__ == "__main__":
    app.run(debug=True)