from datetime import datetime
from .team import Team
from .player import Player

class Action:
    def __init__(self, action_type: str, player: Player, team: Team, location: tuple, game_id: str, timestamp: datetime):
        """
        :param action_type: Type of action (e.g., 'shot', 'goal', 'hit', 'save')
        :param player: Name of the player performing the action
        :param team: Team of the player
        :param location: (x, y) coordinates on the ice rink
        :param game_id: Unique identifier for the game
        :param timestamp: Date and time when the action occurred
        """
        self.action_type = action_type
        self.player = player
        self.team = team
        self.location = location
        self.game_id = game_id
        self.timestamp = timestamp
    
    def __repr__(self):
        return (f"{self.timestamp} - {self.game_id}: {self.player} ({self.team}) "
                f"performed {self.action_type} at location {self.location}")
