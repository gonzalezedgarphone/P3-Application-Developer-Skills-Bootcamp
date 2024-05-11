from dataclasses import dataclass
from models.tournament import Tournament
from pathlib import Path
@dataclass
class TournamentListCmd:
    """
    Command to list all tournaments.
    """
    def __init__(self, tournaments_folder):
        self.tournaments_folder = tournaments_folder

    def __call__(self):
        # Ensure the Tournament class has a method to load tournaments
        tournaments = Tournament.load_tournaments_from_folder(self.tournaments_folder)
        # Assuming 'load_tournaments_from_folder' updates Tournament.tournaments
        return {
            'screen': 'tournament-menu',
            'run': True,
            'tournaments': tournaments
        }
