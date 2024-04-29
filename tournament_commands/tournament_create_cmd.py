from dataclasses import dataclass
from typing import Dict, List
from ..models.tournament import Tournament


@dataclass
class TournamentCreateCmd:
    """
    Command to create a new tournament.
    """
    name: str
    venue: str
    start_date: str
    end_date: str
    num_rounds: int
    players: List[str]
    current_round: int = 0
    rounds: List[List[Dict[str, str]]] = None

    def execute(self):
        dates = {"from": self.start_date, "to": self.end_date}
        new_tournament = Tournament.create_tournament(
            name=self.name,
            dates=dates,
            venue=self.venue,
            number_of_rounds=self.num_rounds,
            current_round=self.current_round,
            players=self.players,
            rounds=self.rounds
        )
        print(f"Tournament '{self.name}' created successfully.")
        return new_tournament
