from objects.action import Action
from objects.game import Game
from objects.player import Player
from objects.team import Team
from common.cache import Cache
import requests
import mysql.connector


player_cache = Cache('player_cache.pkl')
team_cache = Cache('team_cache.pkl')

conn = mysql.connector.connect(
    host="localhost",      # e.g., "localhost"
    user="root",  # e.g., "root"
    password="GoBolts#12358",
    database="nhl_data" # Change to your actual database name
)

cursor = conn.cursor()


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
            data = (
                team_data["conferenceAbbrev"],
                team_data["divisionAbbrev"],
                team_data["gamesPlayed"],
                team_data["goalDifferential"],
                team_data["goalAgainst"],
                team_data["goalFor"],

                team_data["homeGamesPlayed"],
                team_data["homeGoalDifferential"],
                team_data["homeGoalsAgainst"],
                team_data["homeGoalsFor"],
                team_data["homeLosses"],
                team_data["homeOtLosses"],
                team_data["homePoints"],
                team_data["homeRegulationWins"],
                team_data["homeWins"],

                team_data["losses"],
                team_data["otLosses"],
                team_data["placeName"]["default"],  # Extracting nested field
                team_data["pointPctg"],
                team_data["points"],
                team_data["regulationWins"],
                team_data["seasonId"],
                team_data["shootoutLosses"],
                team_data["shootoutWins"],
                team_data["teamName"]["default"],  # Extracting nested field
                team_data["teamAbbrev"]["default"],  # Extracting nested field
                team_data["teamLogo"],
                team_data["ties"],
                team_data["wins"]
            )            
            sql = """INSERT INTO teams (
                conference_abbrev, division_abbrev, games_played, goal_differential, goal_against, goal_for,
                home_games_played, home_goal_differential, home_goals_against, home_goals_for, home_losses, 
                home_ot_losses, home_points, home_regulation_wins, home_wins,
                losses, ot_losses, place_name, point_pctg, points, regulation_wins, season_id, shootout_losses, 
                shootout_wins, team_name, team_abbrev, team_logo, ties, wins
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            cursor.execute(sql, data)
            conn.commit()


def main():
    standings_data = fetch_standings()
    extract_team_data(standings_data)
    

if __name__ == "__main__":
    main()