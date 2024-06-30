from dataclasses import dataclass, field
import os
from datetime import datetime
from typing import List, Dict, Optional, ClassVar
import json
from pathlib import Path
from models.player import Player



MAX_ROUNDS = 4

@dataclass
class PlayerDetails:
    name: str
    email: str
    chess_id: str
    birthday: str
    points: float = 0.0

    def make_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "chess_id": self.chess_id,
            "birthday": self.birthday,
            "points": self.points
        }


DATE_FORMAT = "%d-%m-%Y"
@dataclass
class Tournament:
    name: str
    venue: str
    start_date: str
    end_date: str
    registered_players: List[PlayerDetails]
    num_rounds: int = MAX_ROUNDS
    current_round: int = 1
    completed: Optional[bool] = False
    finished: Optional[bool] = False
    rounds: Optional[List[List[dict]]] = None
    filepath: Optional[Path] = None

    tournaments: ClassVar[List['Tournament']] = []

    def __post_init__(self):
        if self.filepath:
            if os.path.isdir(self.filepath):
                self.load_from_folder()
            else:
                self.load_from_json()
        else:
            '''required_fields = [self.name, self.venue, self.start_date, self.end_date, self.num_rounds, self.current_round]
            if not all(required_fields):
                raise ValueError("Required attributes are missing")'''
            if self.num_rounds > MAX_ROUNDS:
                raise ValueError(f"Number of rounds cannot exceed {MAX_ROUNDS}")


    @classmethod
    def load_from_folder(cls):
        base_dir = Path(__file__).resolve().parent.parent
        folder_path = base_dir / "data" / "tournaments"
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.json'):
                file_path = folder_path / file_name
                tournament = cls.from_json(file_path)
                cls.tournaments.append(tournament)

    @classmethod
    def create_tournament(cls, name: str, dates: Dict[str, str], venue: str, number_of_rounds: int, current_round: int,
                          players: List[str] = None, rounds: List[List[Dict[str, str]]] = None,
                          finished: bool = False):

        tournament = cls(
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
        # Create an instance of the Tournament class and append the new tournament
        instance = cls()
        instance.tournaments.append(tournament)
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
                self.num_rounds = data.get("number_of_rounds", 0)
                self.current_round = data.get("current_round", 0)
                self.completed = data.get("completed", False)
                self.finished = data.get("finished", False)
                self.rounds = data.get("rounds", [])

                # Handle player information format
                self.registered_players = []
                for player in data.get("players", []):
                    if isinstance(player, str):
                        # Player is represented by chess_id only
                        self.registered_players.append(PlayerDetails(name="", email="", chess_id=player, birthday=""))
                    elif isinstance(player, dict):
                        # Player has detailed information
                        self.registered_players.append(PlayerDetails(
                            name=player.get("name", ""),
                            email=player.get("email", ""),
                            chess_id=player.get("chess_id", ""),
                            birthday=player.get("birthday", ""),
                            points=player.get("points", 0)
                        ))
        else:
            raise ValueError("Filepath is not provided")

    def to_dict(self):
        return {
            "name": self.name,
            "venue": self.venue,
            "dates": {"from": self.start_date, "to": self.end_date},
            "players": [player.make_dict() if isinstance(player, PlayerDetails) else player for player in self.registered_players],
            "number_of_rounds": self.num_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "finished": self.finished,
            "rounds": self.rounds,

        }

    @classmethod
    def load_tournaments_from_folder(cls, folder_path):
        tournaments = []
        loaded_tournament_names = set()  # Track loaded tournament names

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.json'):
                file_path = folder_path / file_name
                try:
                    with open(file_path) as fp:
                        tournament_data = json.load(fp)
                        tournament = cls.from_json(file_path)

                        # Check if tournament name already exists
                        if tournament.name in loaded_tournament_names:
                            continue

                        tournaments.append(tournament)
                        loaded_tournament_names.add(tournament.name)

                except json.JSONDecodeError as e:
                    print(f"Error loading JSON file {file_name}: {e}")
                except KeyError as e:
                    print(f"KeyError in JSON file {file_name}: {e}")
                except Exception as e:
                    print(f"An error occurred while processing {file_name}: {e}")

        return tournaments
    @classmethod
    def save_tournaments(cls):
        base_dir = Path(__file__).resolve().parent.parent
        data_folder = base_dir / "data" / "tournaments"
        for tournament in cls.tournaments:
            file_path = data_folder / f"{tournament.name.replace(' ', '_')}.json"
            with open(file_path, "w") as fp:
                json.dump(tournament.to_dict(), fp, indent=4)

    def save(self):
        if self.filepath:
            tournament_data = self.to_dict()
            tournament_data["filepath"] = str(self.filepath)
            with open(self.filepath, 'w') as f:
                json.dump(tournament_data, f, indent=4)
        else:
            print("Filepath not set. Cannot save tournament.")
    def display_all_tournaments(self):
        sorted_tournaments = sorted(self.tournaments, key=lambda t: datetime.strptime(t.start_date,
                                                                                      "%d-%m-%Y") if t.start_date else datetime.min,
                                    reverse=True)

        for i, tournament in enumerate(sorted_tournaments, start=1):
            print(f"Tournament {i}: {tournament.name}")

    @classmethod
    def get_tournament_by_index(cls, index):
        # Logic to retrieve the tournament by index
        # For example:
        if 0 <= index < len(cls.tournaments):
            return cls.tournaments[index]
        else:
            return None

    def register_player(self, player_name: str):
        if player_name not in self.registered_players:
            self.registered_players.append(player_name)

    def display_info(self):
        print("Tournament Information:")
        print(f"Name: {self.name}")
        print(f"Venue: {self.venue}")
        print(f"Start Date: {self.start_date}")
        print(f"End Date: {self.end_date}")
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
                winner = match.get('winner')
                if winner is None:
                    winner_message = "Draw" if completed else "Not Yet Completed"
                else:
                    winner_message = winner
                print(f"  Players: {players}")
                print(f"  Completed: {completed}")
                print(f"  Winner: {winner_message}")
                print()

    def questions(self):
        self.name = input("Enter tournament name: ")
        self.venue = input("Enter tournament venue: ")
        self.start_date = input("Enter tournament start date (DD-MM-YYYY): ")
        self.end_date = input("Enter tournament end date (DD-MM-YYYY): ")
        self.num_rounds = int(input("Enter number of rounds: "))
        self.current_round = int(input("Enter current round: "))

        while True:
            player_name = input("Enter player name: ")
            self.registered_players.append(player_name)

            add_another = input("Add another player? (yes/no): ")
            if add_another.lower() != "yes":
                break

        print(f"Tournament '{self.name}' created successfully.")
        self.save_tournaments()

    @classmethod
    def from_json(cls, filepath: Path):
        with open(filepath) as fp:
            try:
                data = json.load(fp)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON file {filepath}: {e}")
                return None

        # Extract and parse dates
        dates = data.get("dates", {})
        start_date_str = dates.get("from", "")
        end_date_str = dates.get("to", "")

        try:
            # Attempt to parse dates with format %d-%m-%Y
            start_date = datetime.strptime(start_date_str, "%d-%m-%Y").strftime("%d-%m-%y")
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y").strftime("%d-%m-%y")
        except ValueError as e1:
            print(f"Error parsing dates with format %d-%m-%Y: {e1}")
            try:
                # Attempt to parse dates with format %m-%d-%Y
                start_date = datetime.strptime(start_date_str, "%m-%d-%Y").strftime("%d-%m-%y")
                end_date = datetime.strptime(end_date_str, "%m-%d-%Y").strftime("%d-%m-%y")
            except ValueError as e2:
                print(f"Error parsing dates with format %d-%m-%Y: {e2}")
                start_date = end_date = ""  # Handle error case gracefully

        # Handling players
        players_data = data.get("players", [])

        if all(isinstance(player_data, str) for player_data in players_data):
            # Assume chess IDs
            registered_players = [
                PlayerDetails(name="", email="", chess_id=player_data, birthday="")
                for player_data in players_data
            ]
        else:
            # Assume it's detailed player information
            registered_players = [
                PlayerDetails(
                    name=player_data.get("name", ""),
                    email=player_data.get("email", ""),
                    chess_id=player_data.get("chess_id", ""),
                    birthday=player_data.get("birthday", ""),
                    points=player_data.get("points", 0)
                )
                for player_data in players_data
            ]

        # Other fields
        num_rounds = data.get("number_of_rounds", 0)
        current_round = data.get("current_round", 0)
        completed = data.get("completed", False)
        finished = data.get("finished", False)
        rounds = data.get("rounds", [])




        tournament = cls(
            name=data.get("name", ""),
            venue=data.get("venue", ""),
            start_date=start_date,
            end_date=end_date,
            registered_players=registered_players,
            num_rounds=num_rounds,
            current_round=current_round,
            completed=completed,
            finished=finished,
            rounds=rounds,
            filepath=filepath
        )

        cls.tournaments.append(tournament)
        return tournament

    @classmethod
    def prompt_questions(cls):
        name = input("Enter tournament name: ")
        venue = input("Enter tournament venue: ")
        start_date_str = input("Enter tournament start date (DD-MM-YYYY): ")
        end_date_str = input("Enter tournament end date (DD-MM-YYYY): ")

        # Parse dates using the specified format
        start_date = datetime.strptime(start_date_str, DATE_FORMAT).strftime(DATE_FORMAT)
        end_date = datetime.strptime(end_date_str, DATE_FORMAT).strftime(DATE_FORMAT)

        num_rounds = int(input("Enter number of rounds: "))
        current_round = int(input("Enter current round: "))

        registered_players = []

        while len(registered_players) < 2 or input("Add another player? (yes/no): ").lower() == "yes":
            if len(registered_players) < 2:
                print("A tournament must have at least two registered players.")

            player_name = input("Enter player name: ")
            email = input(f"Enter email for {player_name}: ")
            chess_id = input(f"Enter chess ID for {player_name}: ")
            birthday = input(f"Enter birthday for {player_name} (DD-MM-YYYY): ")
            points = float(input(f"Enter points for {player_name}: "))

            player = PlayerDetails(name=player_name, email=email, chess_id=chess_id, birthday=birthday, points=points)
            registered_players.append(player)

        completed_input = input("Enter completed (True/False), or press enter to skip: ")
        completed = bool(completed_input) if completed_input else False

        finished_input = input("Enter finished (True/False), or press enter to skip: ")
        finished = bool(finished_input) if finished_input else False

        rounds = []

        instance = cls(
            name=name,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            registered_players=registered_players,
            num_rounds=num_rounds,
            current_round=current_round,
            completed=completed,
            finished=finished,
            rounds=rounds,
        )

        # Assuming file paths and saving logic remain similar
        base_dir = Path(__file__).resolve().parent.parent
        folder_path = base_dir / "data" / "tournaments"
        file_path = folder_path / f"{instance.name.replace(' ', '_')}.json"

        if not folder_path.exists():
            folder_path.mkdir(parents=True)

        instance.filepath = file_path
        instance.save()

        cls.tournaments.append(instance)
        return instance


def main():
    # Construct the absolute path to the tournaments folder
    folder_path = Path(__file__).resolve().parent.parent / "data" / "tournaments"

    if not folder_path.exists() or not folder_path.is_dir():
        print("Tournaments folder not found or is not a directory.")
        return

    # Use the class method correctly
    tournaments = Tournament.load_tournaments_from_folder(folder_path)

    # Display information about loaded tournaments
    for i, tournament in enumerate(tournaments, start=1):
        print(f"Tournament {i}:")
        tournament.display_info()

    for names in tournaments:
        print(names)

if __name__ == "__main__":
    main()
