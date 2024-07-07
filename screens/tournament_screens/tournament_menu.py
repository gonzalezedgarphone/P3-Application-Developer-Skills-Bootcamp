import os
import json
from pathlib import Path
from ..base_screen import BaseScreen
from commands import NoopCmd
from commands.context import Context
from models.tournament import Tournament, PlayerDetails
from datetime import datetime


class TournamentMenu(BaseScreen):
    """Menu for tournament operations"""

    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.sorted_tournaments = sorted(
            self.tournaments,
            key=lambda t: datetime.strptime(t.start_date, "%d-%m-%Y"),
            reverse=True,
        )

    def display(self):
        print("Tournaments:")
        # Display sorted tournaments
        for idx, tournament in enumerate(self.sorted_tournaments, 1):
            print(
                f"{idx}. {tournament.name} at {tournament.venue} from {tournament.start_date} to "
                f"{tournament.end_date}"
            )

    def get_command(self):
        while True:
            print(
                "Type the number of a tournament to view/manage it, 'E' to edit, 'C' to create a new tournament,"
                " 'L' to see a list of registered players, or 'S' to search for a player."
            )
            print("Type 'X' to exit.")
            value = self.input_string()
            if value.isdigit():
                value = int(value)
                if value in range(1, len(self.sorted_tournaments) + 1):
                    return NoopCmd(
                        "tournament-view", tournament=self.sorted_tournaments[value - 1]
                    )
                else:
                    print("Invalid tournament number.")
            elif value.upper() == "C":
                new_tournament = Tournament.prompt_questions()
                if len(new_tournament.registered_players) < 2:
                    print("A tournament must have at least two players.")
                else:
                    return Context("tournament-create", tournament=new_tournament)
            elif value.upper() == "E":
                tournament_idx = input("Enter the number of the tournament to edit: ")
                if tournament_idx.isdigit():
                    index = int(tournament_idx) - 1
                    if 0 <= index < len(self.sorted_tournaments):
                        # Retrieve the tournament using the index
                        tournament = self.sorted_tournaments[index]

                        # Collect updates for the tournament
                        updates = self.collect_tournament_updates(tournament)
                        # Check if there are at least two registered players
                        if (
                            "registered_players" in updates
                            and len(updates["registered_players"]) < 2
                        ):
                            print(
                                "A tournament must have at least 2 registered players."
                            )
                        else:
                            # Create and execute the update command
                            original_name = tournament.name  # Track the original name
                            self.update_tournament(tournament, **updates)
                            # Check if the tournament name was changed
                            if original_name != tournament.name:
                                self.remove_old_tournament_file(original_name)
                            print(
                                f"Tournament '{tournament.name}' updated successfully."
                            )
                            # Update the sorted list to reflect changes
                            self.sorted_tournaments = sorted(
                                self.tournaments,
                                key=lambda t: datetime.strptime(
                                    t.start_date, "%d-%m-%Y"
                                ),
                                reverse=True,
                            )
                            self.display()
                    else:
                        print("Invalid tournament number.")
                else:
                    print("Invalid tournament number.")
            elif value.upper() == "L":
                self.extract_players()
                self.sorted_tournaments = sorted(
                    self.tournaments,
                    key=lambda t: datetime.strptime(t.start_date, "%d-%m-%Y"),
                    reverse=True,
                )
                self.display()
            elif value.upper() == "S":
                tournament_idx = input(
                    "Enter the number of the tournament to search players in: "
                )
                if tournament_idx.isdigit():
                    index = int(tournament_idx) - 1
                    if 0 <= index < len(self.sorted_tournaments):
                        tournament = self.sorted_tournaments[index]
                        self.search_player(tournament)
                    else:
                        print("Invalid tournament number.")
                else:
                    print("Invalid tournament number.")
            elif value.upper() == "X":
                return Context(run=False)

    @staticmethod
    def collect_tournament_updates(tournament):
        """Collect updates for an existing tournament."""
        updates = {}

        print(
            f"Enter updates for tournament '{tournament.name}' (press enter to skip): "
        )
        for key, value in tournament.__dict__.items():
            if key == "registered_players":
                updated_players = []
                for player in value:
                    print(f"\nCurrent player: {player.name}")
                    new_name = input(
                        f"Enter new value for name (current: {player.name}): "
                    )
                    new_email = input(
                        f"Enter new value for email (current: {player.email}): "
                    )
                    new_chess_id = input(
                        f"Enter new value for chess_id (current: {player.chess_id}): "
                    )
                    new_birthday = input(
                        f"Enter new value for birthday (current: {player.birthday}): "
                    )

                    updated_player = PlayerDetails(
                        name=new_name or player.name,
                        email=new_email or player.email,
                        chess_id=new_chess_id or player.chess_id,
                        birthday=new_birthday or player.birthday,
                        points=player.points,
                    )
                    updated_players.append(updated_player)
                updates[key] = updated_players
            elif key == "rounds":
                # Display current rounds information
                print("Current rounds: ")
                for i, round_info in enumerate(value, start=1):
                    print(f"Round {i}: ")
                    for match in round_info:
                        players = match["players"]
                        completed = match["completed"]
                        winner = match.get("winner")
                        if winner is None:
                            winner_message = (
                                "Draw" if completed else "Not Yet Completed"
                            )
                        else:
                            winner_message = winner
                        print(f"  Players: {players}")
                        print(f"  Completed: {completed}")
                        print(f"  Winner: {winner_message}")
                        print()

                # Ask for new rounds input
                new_rounds = []
                while True:
                    round_input = input(
                        "Enter new round information (or leave empty to finish): "
                    )
                    if not round_input:
                        break
                    # Parse and validate round_input if needed
                    # For simplicity, assume round_input is properly formatted
                    new_rounds.append(
                        json.loads(round_input)
                    )  # Example: [{'players': ['JE33355', 'JP9345'], 'completed': False}]
                updates[key] = new_rounds
            elif key == "current_round":
                new_value = input(f"Enter new value for {key} (current: {value}): ")
                if new_value.strip() == "":
                    # User skipped entering a value, no update needed
                    pass
                elif new_value.isdigit():
                    updates[key] = int(
                        new_value
                    )  # Ensure current_round is stored as an integer
                else:
                    print("Invalid input. Please enter a valid integer.")
            else:
                new_value = input(f"Enter new value for {key} (current: {value}): ")
                if new_value:
                    updates[key] = new_value

        return updates

    def update_tournament(self, tournament, **kwargs):
        """Utility method to update a tournament instance based on arguments provided"""
        if tournament not in self.tournaments:
            raise RuntimeError(f"Tournament {tournament.name} not in the list!")

        for key, value in kwargs.items():
            setattr(tournament, key, value)

        # Update the filepath after renaming
        if "name" in kwargs:
            old_filepath = tournament.filepath
            new_filename = f"{kwargs['name'].replace(' ', '_')}.json"
            new_filepath = old_filepath.parent / new_filename
            tournament.filepath = new_filepath

        self.save_tournaments()

    @staticmethod
    def remove_old_tournament_file(tournament_name):
        """Remove the old tournament JSON file if the name was changed"""
        try:
            base_dir = Path(__file__).resolve().parent.parent.parent
            data_folder = base_dir / "data" / "tournaments"
            old_filename = f"{tournament_name.replace(' ', '_')}.json"
            file_path = data_folder / old_filename
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Old tournament file '{file_path}' removed successfully.")
            else:
                print(
                    f"No file found for the old tournament name '{file_path}' to remove."
                )
        except Exception as e:
            print(f"An error occurred while removing the old tournament file: {e}")

    @staticmethod
    def save_tournaments():
        """Save all tournaments to their respective JSON files"""
        Tournament.save_tournaments()

    @staticmethod
    def search_player(tournament):
        """Search for a player within a specific tournament."""
        search_term = (
            input("Enter the Chess ID or part of the player's name to search: ")
            .strip()
            .lower()
        )

        found_players = [
            player
            for player in tournament.registered_players
            if search_term in player.chess_id.lower()
            or search_term in player.name.lower()
        ]

        if found_players:
            print("\nSearch results:")
            for idx, player in enumerate(found_players, 1):
                print(f"{idx}. {player.name} (Chess ID: {player.chess_id})")
        else:
            print("No players found matching the search criteria.")

    @staticmethod
    def load_tournament_data():
        """Load tournament data from JSON files."""
        base_dir = Path(__file__).resolve().parent.parent.parent
        data_folder = base_dir / "data" / "tournaments"
        tournament_files = data_folder.glob("*.json")

        tournaments = []
        for file_path in tournament_files:
            tournament = Tournament.from_json(file_path)
            if tournament:
                tournaments.append(tournament)

        return tournaments

    def extract_players(self):
        tournaments = self.load_tournament_data()
        for tournament in tournaments:
            print(f"\nTournament: {tournament.name}")
            if tournament.registered_players:
                print("Registered Players:")
                for player in tournament.registered_players:
                    print(f"Name: {player.name}, Chess ID: {player.chess_id}")
            else:
                print("No registered players in this tournament.")
