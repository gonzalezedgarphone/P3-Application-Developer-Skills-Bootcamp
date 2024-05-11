from dataclasses import dataclass
from models.tournament import Tournament


@dataclass
class TournamentViewCmd:
    """
    Command to view a specific tournament's details.
    """
    index: int

    def execute(self):
        tournament = Tournament.get_tournament_by_index(self.index)
        if not tournament:
            print("Tournament not found.")
            return None

        tournament.display_info()
        return tournament
