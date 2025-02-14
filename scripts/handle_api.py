import sys
sys.path.append(".")
import requests
from xml.etree import ElementTree as ET
from time import sleep, time
from app.models.game import db, BoardGame, Feature
from flask import Flask
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace("sqlite:///", "sqlite:///"+os.path.abspath(os.getcwd())+"/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

BGG_API_DELAY = 2

db.init_app(app)

def add_features():
    games = BoardGame.query.all()
    counter = 0
    search_ids = ""
    for game in games:
        search_ids += str(game.id) + ","
        counter += 1
        if counter % 20 == 0 or counter == len(games):
            search_ids = search_ids[:-1]
            start = time()
            game_features = game_details(search_ids)
            search_ids = ""

            for game_id, features_list in game_features.items():
                print(f"{game_id}: {[feature[1] for feature in features_list]}")
                for game_feature in features_list:
                    feature = Feature.query.filter_by(id=game_feature[0]).first()
                    
                    if not feature:  # If the feature isn't already in the database
                        feature = Feature(id=game_feature[0], name=game_feature[1])
                        db.session.add(feature)
                        db.session.commit()
                    
                    current_game = BoardGame.query.filter_by(id=game_id).first()
                    if feature not in current_game.features:
                        current_game.features.append(feature)
                db.session.commit()
            end = time()
            time_taken = round(end - start, 2)
            if time_taken < BGG_API_DELAY:
                sleep(BGG_API_DELAY - time_taken)
            print(f"Time taken: {time_taken} seconds")


def game_details(game_ids):
    game_features = {}
    attempts = 0
    url = f"https://www.boardgamegeek.com/xmlapi2/thing?id={game_ids}"
    response = requests.get(url)
    while response.status_code != 200:
        attempts += 1
        if attempts > 5:
            raise Exception("Continuous errors fetching data")
        print("Error fetching data")
        sleep(BGG_API_DELAY * attempts)  # Longer and longer delay
        response = requests.get(url)
    tree = ET.fromstring(response.content)
    all_board_games = tree.findall("item")
    for board_game in all_board_games:
        game_id = board_game.get("id")
        features = []
        for link in board_game.findall("link"):
            if link.get("type") == "boardgamemechanic" or link.get("type") == "boardgamecategory":
                features.append([int(link.get("id")), link.get("value")])  # Must make sure that the id is an integer
        game_features[game_id] = features
    return game_features


if __name__ == "__main__":
    with app.app_context():
        add_features()
