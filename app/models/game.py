from app.extensions import db

class BoardGameMechanic(db.Model):
    __tablename__ = "board_game_mechanics"

    board_game_id = db.Column(db.Integer, db.ForeignKey("board_game.id"), primary_key=True, nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey("mechanic.id"), primary_key=True, nullable=False)


class BoardGame(db.Model):
    __tablename__ = "board_game"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    usersrated = db.Column(db.Integer, nullable=False)
    mechanics = db.relationship(
        "Mechanic", # Related model
        secondary="board_game_mechanics", # Association table
        back_populates="board_games" # Name of relationship in related model
    )

class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    board_games = db.relationship(
        "BoardGame", # Related model
        secondary="board_game_mechanics", # Association table
        back_populates="mechanics" # Name of relationship in related model
    )

