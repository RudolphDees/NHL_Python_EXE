from player import Player
from typing import List

class Team:
    def __init__(self, name: str, city: str, conference: str, division: str, arena: str, 
                 championships: int = 0, roster: List[Player] = None, coach: str = "Unknown", team_id: str = ""):
        self.name = name
        self.city = city
        self.conference = conference
        self.division = division
        self.arena = arena
        self.championships = championships
        self.roster = roster if roster is not None else []
        self.coach = coach
        self.team_id = team_id
    
    def add_player(self, player: Player):
        self.roster.append(player)
    
    def remove_player(self, player_name: str):
        self.roster = [player for player in self.roster if player.name != player_name]
    
    def update_championships(self, count: int):
        self.championships = count
    
    def update_coach(self, coach_name: str):
        self.coach = coach_name
    
    def get_team_info(self):
        return {
            "name": self.name,
            "city": self.city,
            "conference": self.conference,
            "division": self.division,
            "arena": self.arena,
            "championships": self.championships,
            "coach": self.coach,
            "roster": [repr(player) for player in self.roster]
        }
