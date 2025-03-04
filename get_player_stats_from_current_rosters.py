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
    url = f"https://api-web.nhle.com/v1/roster/TOR/current"
    response = requests.get(url)

    if response.status_code == 200:
        standings_data = response.json()
        return standings_data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def extract_roster_data():
    team_name_list = team_cache.load_cache()
    team_list: list[Team] = []
    for team_name in team_name_list:
        team_list.append(team_cache.get(team_name))

    for team in team_list:
        print(f"Extracting player data for {team.get_team_name()}")
        url = f"https://api-web.nhle.com/v1/roster/{team.get_team_abr()}/current"
        response = requests.get(url)

        if response.status_code == 200:
            roster_data = response.json()
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
        for player in roster_data.get("forwards", []):
            player_info = {
                "player_id": player["id"]
            } 
            player_cache.set(player["id"], Player(player["id"], player_info))
        for player in roster_data.get("defensemen", []):
            player_info = {
                "player_id": player["id"]
            } 
            player_cache.set(player["id"], Player(player["id"], player_info))
        for player in roster_data.get("goalies", []):
            player_info = {
                "player_id": player["id"]
            } 
            player_cache.set(player["id"], Player(player["id"], player_info))

    

    

def main():
    extract_roster_data()
    

if __name__ == "__main__":
    main()