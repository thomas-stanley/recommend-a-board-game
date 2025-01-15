import requests
from xml.etree import ElementTree as ET
from time import sleep


def game_details(game_id):
    url = f"https://www.boardgamegeek.com/xmlapi2/thing?id={game_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching data")
        return None
    else:
        tree = ET.fromstring(response.content)
        board_game = tree.find("item")
        mechanics = []
        for link in board_game.findall("link"):
            if link.get("type") == "boardgamemechanic":
                mechanics.append(link.get("value"))
        return mechanics

def recommend_games(games_to_check, weighted_mechanics, user_games):
    recommended_games = []
    for game in games_to_check.iterrows():
        if game[1]["name"] not in user_games:
            url = f"https://www.boardgamegeek.com/xmlapi2/thing?id={game[1]["id"]}"
            response = requests.get(url)
            if response.status_code != 200:
                print("Error fetching data")
                continue
            else:
                tree = ET.fromstring(response.content)
                board_game = tree.find("item")
                mechanics = []
                for link in board_game.findall("link"):
                    if link.get("type") == "boardgamemechanic":
                        game_mechanic = link.get("value")
                        if game_mechanic in weighted_mechanics:
                            mechanics.append(game_mechanic)
                score = 0
                for mechanic in mechanics:
                    score += weighted_mechanics[mechanic]
                print(f"Game: {game[1]['name']}, Score: {score}")
                if score > 2:  # Minimum score to be recommended
                    recommended_games.append((game[1]["name"], score))
            sleep(0.5)
    sorted_games = sorted(recommended_games, key=lambda x: x[1], reverse=True)
    return sorted_games


def main():
    print(game_details(30549))  # Pandemic

if __name__ == "__main__":
    main()