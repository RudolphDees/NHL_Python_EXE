from typing import List

class Team:
    def __init__(self, name: str, 
                 roster, team_data):
        self.name = name
        self.roster = roster if roster is not None else []
        self.team_data = team_data
    
    def get_team_info(self):
        return {
            "name": self.name,
            "roster": [repr(player) for player in self.roster]
        }
    def get_team_abr(self):
        return self.team_data["teamAbbrev"]["default"]

    def get_team_name(self):
        return self.team_data["teamName"]["default"]