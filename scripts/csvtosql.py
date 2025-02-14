import sys
sys.path.append(".")
from flask import Flask
import pandas as pd
from app.models.game import db, BoardGame
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace("sqlite:///", "sqlite:///"+os.path.abspath(os.getcwd())+"/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    df = pd.read_csv("data/cleaned_boardgames_ranks.csv")

    for bg_index, row in df.iterrows():
        board_game = BoardGame(
            id=row["id"], 
            name=row["name"], 
            bayesaverage=row["bayesaverage"],
            usersrated=row["usersrated"],
            is_expansion=row["is_expansion"]
            )


        db.session.add(board_game)
    db.session.commit()
