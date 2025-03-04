from datetime import datetime
from action import Action
from team import Team

class Game:
    def __init__(self, game_id: str, home_team: Team, away_team: Team, venue: str, game_date: datetime, actions: list = None):
        """
        :param game_id: Unique identifier for the game
        :param home_team: Name of the home team
        :param away_team: Name of the away team
        :param venue: Location where the game is played
        :param game_date: Date and time of the game
        :param actions: List of in-game actions (instances of Action)
        """
        self.game_id = game_id
        self.home_team = home_team
        self.away_team = away_team
        self.venue = venue
        self.game_date = game_date
        self.actions = actions if actions is not None else []
    
    def add_action(self, action):
        """Adds a Action to the game."""
        self.actions.append(action)
    
    def __repr__(self):
        return (f"Game {self.game_id}: {self.away_team} at {self.home_team}, "
                f"Venue: {self.venue}, Date: {self.game_date}, "
                f"Total Actions: {len(self.actions)}")
