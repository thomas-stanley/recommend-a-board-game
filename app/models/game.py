from app.extensions import db

class BoardGameFeature(db.Model):
    __tablename__ = "board_game_features"

    board_game_id = db.Column(db.Integer, db.ForeignKey("board_game.id"), primary_key=True, nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey("feature.id"), primary_key=True, nullable=False)


class BoardGame(db.Model):
    __tablename__ = "board_game"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    bayesaverage = db.Column(db.Float, nullable=False)
    usersrated = db.Column(db.Integer, nullable=False)
    is_expansion = db.Column(db.Boolean, nullable=False)
    features = db.relationship(
        "Feature", # Related model
        secondary="board_game_features", # Association table
        back_populates="board_games" # Name of relationship in related model
    )

class Feature(db.Model):
    __tablename__ = "feature"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    board_games = db.relationship(
        "BoardGame", # Related model
        secondary="board_game_features", # Association table
        back_populates="features" # Name of relationship in related model
    )

