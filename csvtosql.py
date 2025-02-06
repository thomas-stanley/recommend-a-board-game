from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/boardgames.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class BoardGame(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    usersrated = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

    df = pd.read_csv("data/cleaned_boardgames_ranks.csv")
    print(df.columns)

    for bg_index, row in df.iterrows():
        board_game = BoardGame(
            id=row["id"], 
            name=row["name"], 
            rank=row["rank"], 
            usersrated=row["usersrated"]
            )


        db.session.add(board_game)
    print(BoardGame.query.all())
    db.session.commit()
