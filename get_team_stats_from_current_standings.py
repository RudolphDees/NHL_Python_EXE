from objects.action import Action
from objects.game import Game
from objects.player import Player
from objects.team import Team
from common.cache import Cache
import requests
import json

player_cache = Cache('player_cache.pkl')
team_cache = Cache('team_cache.pkl')


def fetch_standings():
    url = "https://api-web.nhle.com/v1/standings/now"
    response = requests.get(url)

    if response.status_code == 200:
        standings_data = response.json()
        return standings_data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def extract_team_data(standings_data):
    if standings_data:
        for team_data in standings_data.get("standings", []):
            team_info = {
                "team_name": team_data["teamName"]["default"]
            }
            team_cache.set(team_info["team_name"], Team(team_info["team_name"], [], team_data))
            print(f"Saving this teams data now: {team_info['team_name']} ")

def main():
    standings_data = fetch_standings()
    extract_team_data(standings_data)
    

if __name__ == "__main__":
    main()