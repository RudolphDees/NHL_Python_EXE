from team import Team

class Player:
    def __init__(self, name: str, position: str, number: int, team: Team, player_id: str):
        self.name = name
        self.position = position
        self.number = number
        self.team = team
        self.player_id = player_id

    def __repr__(self):
        return f"{self.name} ({self.position}, #{self.number}) - {self.team.name}"