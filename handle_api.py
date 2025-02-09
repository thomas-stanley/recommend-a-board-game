import requests
from xml.etree import ElementTree as ET
from time import sleep, time
from app.models.game import db, BoardGame, Mechanic
from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/boardgames.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

BGG_API_DELAY = 2

db.init_app(app)

def add_mechanics():
    games = BoardGame.query.all()
    counter = 0
    search_ids = ""
    for game in games:
        search_ids += str(game.id) + ","
        counter += 1
        if counter % 20 == 0 or counter == len(games):
            search_ids = search_ids[:-1]
            start = time()
            game_mechanics = game_details(search_ids)
            search_ids = ""

            for game_id, mechanics_list in game_mechanics.items():
                print(f"{game_id}: {[mechanic[1] for mechanic in mechanics_list]}")
                for mechanic in mechanics_list:
                    mechanic = Mechanic.query.filter_by(id=mechanic[0]).first()
                    
                    if not mechanic:  # If the mechanic isn't already in the database
                        mechanic = Mechanic(id=mechanic[0], name=mechanic[1])
                        db.session.add(mechanic)
                        db.session.commit()
                    
                    if mechanic not in game.mechanics:
                        game.mechanics.append(mechanic)
                db.session.commit()
            end = time()
            time_taken = round(end - start, 2)
            print(f"Time taken: {time_taken} seconds")
            sleep(BGG_API_DELAY - time_taken)  # Prevent throttling


def game_details(game_ids):
    game_mechanics = {}
    attempts = 0
    url = f"https://www.boardgamegeek.com/xmlapi2/thing?id={game_ids}"
    response = requests.get(url)
    while response.status_code != 200:
        attempts += 1
        if attempts > 5:
            raise Exception("Continuous errors fetching data")
        print("Error fetching data")
        sleep(BGG_API_DELAY * 5 * attempts)  # Longer and longer delay
        response = requests.get(url)
    tree = ET.fromstring(response.content)
    all_board_games = tree.findall("item")
    for board_game in all_board_games:
        game_id = board_game.get("id")
        mechanics = []
        for link in board_game.findall("link"):
            if link.get("type") == "boardgamemechanic":
                mechanics.append([int(link.get("id")), link.get("value")])  # Must make sure that the id is an integer
        game_mechanics[game_id] = mechanics
    return game_mechanics
