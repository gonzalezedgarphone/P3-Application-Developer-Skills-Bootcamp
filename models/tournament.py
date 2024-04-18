from dataclasses import dataclass, field
import os
from datetime import datetime
from typing import List, Dict, Optional
import json
from pathlib import Path
from player import Player

MAX_ROUNDS = 4

@dataclass
class Tournament:
    name: str
    venue: str
    start_date: str
    end_date: str
    registered_players: List[Player]
    num_rounds: int = MAX_ROUNDS
    current_round: int = 0
    completed: Optional[bool] = False
    finished: Optional[bool] = False
    rounds: Optional[List[List[dict]]] = None
    filepath: Optional[Path] = None

    tournaments: List['Tournament'] = field(default_factory=list)

    def __post_init__(self):
        if self.filepath:
            if os.path.isdir(self.filepath):
                self.load_from_folder()
            else:
                self.load_from_json()
        else:
            required_fields = [self.name, self.venue, self.start_date, self.end_date, self.num_rounds, self.current_round]
            if not all(required_fields):
                raise ValueError("Required attributes are missing")
            if self.num_rounds > MAX_ROUNDS:
                raise ValueError(f"Number of rounds cannot exceed {MAX_ROUNDS}")

    @classmethod
    def from_json(cls, filepath: Path):
        with open(filepath) as fp:
            data = json.load(fp)
        tournament = cls(
            name=data.get("name", ""),
            venue=data.get("venue", ""),
            start_date=data["dates"].get("from", ""),
            end_date=data["dates"].get("to", ""),
            registered_players=data.get("players", []),
            num_rounds=data.get("number_of_rounds", 0),
            current_round=data.get("current_round", 0),
            completed=data.get("completed", False),
            finished=data.get("finished", False),
            rounds=data.get("rounds", []),
            filepath=filepath
        )
        tournament.tournaments.append(tournament)  # Append the created tournament to the tournaments list
        return tournament

    @classmethod
    def load_from_folder(cls):
        base_dir = Path(__file__).resolve().parent.parent
        folder_path = base_dir / "data" / "tournaments"
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.json'):
                file_path = folder_path / file_name
                tournament = cls.from_json(file_path)
                cls.tournaments.append(tournament)

    def create_tournament(self, name: str, dates: Dict[str, str], venue: str, number_of_rounds: int, current_round: int,
                          players: List[str] = None, rounds: List[List[Dict[str, str]]] = None,
                          finished: bool = False):

        tournament = Tournament(
            name=name,
            venue=venue,
            start_date=dates["from"],
            end_date=dates["to"],
            registered_players=players or [],
            num_rounds=number_of_rounds,
            current_round=current_round,
            completed=not bool(rounds),  # Assume completed if rounds are provided
            finished=finished,
            rounds=rounds or []
        )
        self.tournaments.append(tournament)
        return tournament  # Return the created tournament object
    #ABLE TO UPDATE AND LOAD FROM JSON FILE
    def load_from_json(self):
        if self.filepath:
            with open(self.filepath) as fp:
                data = json.load(fp)
                self.name = data.get("name", "")
                self.venue = data.get("venue", "")
                self.start_date = data["dates"].get("from", "")
                self.end_date = data["dates"].get("to", "")
                self.registered_players = data.get("players", [])
                self.num_rounds = data.get("number_of_rounds", 0)
                self.current_round = data.get("current_round", 0)
                self.completed = data.get("completed", False)
                self.finished = data.get("finished", False)
                self.rounds = data.get("rounds", [])
        else:
            raise ValueError("Filepath is not provided")

    def to_dict(self):
        return {
            "name": self.name,
            "venue": self.venue,
            "dates": {"from": self.start_date, "to": self.end_date},
            "players": self.registered_players,
            "number_of_rounds": self.num_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "finished": self.finished,
            "rounds": self.rounds
        }

    @classmethod
    def load_tournaments_from_folder(cls, folder_path):
        tournaments = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.json'):
                file_path = folder_path / file_name
                try:
                    with open(file_path) as fp:
                        tournament_data = json.load(fp)
                        tournament = cls.from_json(file_path)
                        tournaments.append(tournament)
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON file {file_name}: {e}")
                except Exception as e:
                    print(f"An error occurred while processing {file_name}: {e}")
        return tournaments

    def save_tournaments(self):
        base_dir = Path(__file__).resolve().parent.parent  # base directory load_from_folder
        data_folder = base_dir / "data" / "tournaments"  # path to tournaments folder
        for tournament in self.tournaments:
            file_path = data_folder / f"{tournament.name.replace(' ', '_')}.json"
            with open(file_path, "w") as fp:
                json.dump(tournament.to_dict(), fp, indent=4)

    def display_all_tournaments(self):
        sorted_tournaments = sorted(self.tournaments, key=lambda t: datetime.strptime(t.start_date,
                                                                                      "%d-%m-%Y") if t.start_date else datetime.min,
                                    reverse=True)

        for i, tournament in enumerate(sorted_tournaments, start=1):
            print(f"Tournament {i}: {tournament.name}")

    def get_tournament_by_index(self, index: int) -> Optional['Tournament']:
        if 1 <= index <= len(self.tournaments):
            return self.tournaments[index - 1]
        else:
            print("Invalid tournament index.")
            return None

    def register_player(self, **player_attrs):
        new_player = Player(**player_attrs)
        player_set = set(self.registered_players)
        player_set.add(new_player)
        self.registered_players = list(player_set)

    def display_info(self):
        print("Tournament Information:")
        print(f"Name: {self.name}")
        print(f"Venue: {self.venue}")
        print(f"Start Date: {self.start_date}")
        print(f"End Date: {self.end_date}")
        # Print each player's information using their __str__ method
        print("Registered Players:")
        for player in self.registered_players:
            print(player)
        print(f"Number of Rounds: {self.num_rounds}")
        print(f"Current Round: {self.current_round}")
        print(f"Completed: {self.completed}")
        print(f"Finished: {self.finished}")
        print("")
        print("Rounds:")
        for i, round_info in enumerate(self.rounds, start=1):
            print(f"Round {i}:")
            for match in round_info:
                players = match['players']
                completed = match['completed']
                winner = match.get('winner')  # Get the winner or None if not present
                if winner is None:
                    winner_message = "Draw" if completed else "Not Yet Completed"
                else:
                    winner_message = winner
                print(f"  Players: {players}")
                print(f"  Completed: {completed}")
                print(f"  Winner: {winner_message}")
                print()






def main():

    folder_path = Path(__file__).resolve().parent.parent / "data" / "tournaments"

    if not folder_path.exists() or not folder_path.is_dir():
        print("Tournaments folder not found or is not a directory.")
        return


    tournaments = Tournament.load_tournaments_from_folder(folder_path)


    for i, tournament in enumerate(tournaments, start=1):
        print(f"Tournament {i}:")
        tournament.display_info()

if __name__ == "__main__":
    main()
