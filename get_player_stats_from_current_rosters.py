from objects.action import Action
from objects.game import Game
from objects.player import Player
from objects.team import Team
from common.cache import Cache
import requests
import json
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
            send_data_to_server(player, team.get_team_abr())

        for player in roster_data.get("defensemen", []):
            send_data_to_server(player, team.get_team_abr())

        for player in roster_data.get("goalies", []):
            send_data_to_server(player, team.get_team_abr())

    

def send_data_to_server(player, team_id):
    if "sweaterNumber" not in player:
        return
    data = (
        player["id"],
        player["firstName"]["default"],
        player["lastName"]["default"],
        player["sweaterNumber"],
        player["positionCode"],
        player["shootsCatches"],
        player["heightInInches"],
        player["weightInPounds"],
        player["heightInCentimeters"],
        player["weightInKilograms"],
        player["birthDate"],
        player["birthCity"]["default"],  # Extracting nested field
        player["birthCountry"],
        team_id,

    )
    update_data = (
        player["firstName"]["default"],
        player["lastName"]["default"],
        player["sweaterNumber"],
        player["positionCode"],
        player["shootsCatches"],
        player["heightInInches"],
        player["weightInPounds"],
        player["heightInCentimeters"],
        player["weightInKilograms"],
        player["birthDate"],
        player["birthCity"]["default"],  # Extracting nested field
        player["birthCountry"],
        team_id,
        player["id"],
    )
    cursor.execute("SELECT id FROM players WHERE id = %s", (player["id"],))
    result = cursor.fetchone()

    if result:
        # If player exists, update the existing record
        sql_update = """UPDATE players SET 
            first_name = %s, 
            last_name = %s, 
            sweater_number = %s, 
            position_code = %s, 
            shoots_catches = %s, 
            height_in_inches = %s, 
            weight_in_pounds = %s, 
            height_in_centimeters = %s, 
            weight_in_kilograms = %s, 
            birth_date = %s, 
            birth_city = %s, 
            birth_country = %s,
            team_abr = %s
            WHERE id = %s"""

        cursor.execute(sql_update, update_data)
        print("✅ Player data updated successfully!")
    else:
        # If player does not exist, insert a new record
        sql_insert = """INSERT INTO players (
            id, first_name, last_name, sweater_number, position_code, shoots_catches,
            height_in_inches, weight_in_pounds, height_in_centimeters, weight_in_kilograms, birth_date,
            birth_city, birth_country, team_abr
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(sql_insert, data)
        print("✅ Player data inserted successfully!")
    conn.commit()

def main():
    extract_roster_data()
    

if __name__ == "__main__":
    main()