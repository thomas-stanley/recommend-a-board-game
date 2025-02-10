import os
from flask import Flask
from config import config
from app.models import game
from app.extensions import db, migrate

def create_app():

    config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import board_games
    app.register_blueprint(board_games)

    return app