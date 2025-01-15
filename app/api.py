import requests
from xml.etree import ElementTree as ET


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

def main():
    print(game_details(30549))  # Pandemic

if __name__ == "__main__":
    main()