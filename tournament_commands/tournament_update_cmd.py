from dataclasses import dataclass
from typing import Dict
from ..models.tournament import Tournament


@dataclass
class TournamentUpdateCmd:
    """
    Command to update an existing tournament.
    """
    index: int
    updates: Dict[str, any]

    def execute(self):
        tournament = Tournament.get_tournament_by_index(self.index)
        if not tournament:
            print("Tournament not found.")
            return None

        for key, value in self.updates.items():
            if hasattr(tournament, key):
                setattr(tournament, key, value)
        print(f"Tournament '{tournament.name}' updated successfully.")
        return tournament
