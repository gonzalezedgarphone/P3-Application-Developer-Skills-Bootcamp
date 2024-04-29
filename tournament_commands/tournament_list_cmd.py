from dataclasses import dataclass
from ..models.tournament import Tournament

class TournamentListCmd:
    """
    Command to list all tournaments.
    """
    def __call__(self):
        # Ensure the Tournament class has a method to load tournaments
        tournaments = Tournament.load_tournaments_from_folder("path/to/tournaments")
        # Assuming 'load_tournaments_from_folder' updates Tournament.tournaments
        return {
            'screen': 'tournament-menu',
            'run': True,
            'tournaments': tournaments  # This should be the actual list of Tournament instances
        }