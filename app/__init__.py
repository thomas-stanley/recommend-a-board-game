import os
from flask import Flask
from config import config

def create_app():

    config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    from app.routes import board_games
    app.register_blueprint(board_games)

    return app