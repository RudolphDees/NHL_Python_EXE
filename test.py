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
    teams = []
    if standings_data:
        for team_data in standings_data.get("standings", []):
            team_info = {
                "team_id": team_data["teamId"],  # Added teamId
                "team_name": team_data["teamName"]["default"],
                "team_abbrev": team_data["teamAbbrev"]["default"],
                "games_played": team_data["gamesPlayed"],
                "points": team_data["points"],
                "wins": team_data["wins"],
                "losses": team_data["losses"],
                "goal_differential": team_data["goalDifferential"],
                "home_wins": team_data["homeWins"],
                "road_wins": team_data["roadWins"],
                "team_logo": team_data["teamLogo"],
            }
            teams.append(team_info)
    return teams

def main():
    standings_data = fetch_standings()
    teams = extract_team_data(standings_data)
    
    if teams:
        print("Team Data Extracted:")
        for team in teams:
            print(f"Team ID: {team['team_id']}")
            print(f"Team: {team['team_name']} ({team['team_abbrev']})")
            print(f"Games Played: {team['games_played']}")
            print(f"Points: {team['points']}")
            print(f"Wins: {team['wins']} - Losses: {team['losses']}")
            print(f"Goal Differential: {team['goal_differential']}")
            print(f"Home Wins: {team['home_wins']} - Road Wins: {team['road_wins']}")
            print(f"Team Logo: {team['team_logo']}")
            print("-" * 30)
    else:
        print("No team data available.")

if __name__ == "__main__":
    main()