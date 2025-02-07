from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BoardGame(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    usersrated = db.Column(db.Integer, nullable=False)