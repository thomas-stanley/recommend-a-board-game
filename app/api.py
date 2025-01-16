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
    to_search = []
    counter = 0  # Counter for splitting the searches into twenties due to api max limit
    search_ids = ""
    for game in games_to_check.iterrows():
        search_ids += str(game[1]["id"]) + ","
        counter += 1
        if counter % 20 == 0 or counter == len(games_to_check):
            search_ids = search_ids[:-1]
            to_search.append(search_ids)
            search_ids = ""

    for search in to_search:
        url = f"https://www.boardgamegeek.com/xmlapi2/thing?id={search}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching data")
            continue
        else:
            tree = ET.fromstring(response.content)
            all_board_games = tree.findall("item")
            for board_game in all_board_games:
                game_name = board_game.find("name").get("value")
                if game_name not in user_games:
                    mechanics = []
                    for link in board_game.findall("link"):
                        if link.get("type") == "boardgamemechanic":
                            game_mechanic = link.get("value")
                            if game_mechanic in weighted_mechanics:
                                mechanics.append(game_mechanic)
                    score = 0
                    for mechanic in mechanics:
                        score += weighted_mechanics[mechanic]
                    print(f"Game: {game_name}, Score: {score}")
                    if score > 0:  # Minimum score to be recommended
                        recommended_games.append((game_name, score))
        sleep(1)
    sorted_games = sorted(recommended_games, key=lambda x: x[1], reverse=True)
    print(sorted_games)
    return sorted_games


def main():
    print(game_details(30549))  # Pandemic

if __name__ == "__main__":
    main()