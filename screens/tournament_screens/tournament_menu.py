import os
from pathlib import Path
from ..base_screen import BaseScreen
from commands import NoopCmd
from commands.context import Context
from commands.tournament_update_cmd import TournamentUpdateCmd
from models.tournament import Tournament
from datetime import datetime

class TournamentMenu(BaseScreen):
    """Menu for tournament operations"""

    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.sorted_tournaments = sorted(self.tournaments, key=lambda t: datetime.strptime(t.start_date, "%d-%m-%Y"),
                                         reverse=True)

    def display(self):
        print("Tournaments:")
        # Display sorted tournaments
        for idx, tournament in enumerate(self.sorted_tournaments, 1):
            print(f"{idx}. {tournament.name} at {tournament.venue} from {tournament.start_date} to {tournament.end_date}")

    def get_command(self):
        while True:
            print("Type the number of a tournament to view/manage it, 'E' to edit, or 'C' to create a new tournament.")
            print("Type 'X' to exit.")
            value = self.input_string()
            if value.isdigit():
                value = int(value)
                if value in range(1, len(self.sorted_tournaments) + 1):
                    return NoopCmd("tournament-view", tournament=self.sorted_tournaments[value - 1])
                else:
                    print("Invalid tournament number.")
            elif value.upper() == 'C':
                new_tournament = Tournament.prompt_questions()
                if len(new_tournament.registered_players) < 2:
                    print("A tournament must have at least two players.")
                else:
                    return Context("tournament-create", tournament=new_tournament)
            elif value.upper() == 'E':
                tournament_idx = input("Enter the number of the tournament to edit: ")
                if tournament_idx.isdigit():
                    index = int(tournament_idx) - 1
                    if 0 <= index < len(self.sorted_tournaments):
                        # Retrieve the tournament using the index
                        tournament = self.sorted_tournaments[index]

                        # Collect updates for the tournament
                        updates = self.collect_tournament_updates(tournament)
                        # Check if there are at least two registered players
                        if 'registered_players' in updates and len(updates['registered_players']) < 2:
                            print("A tournament must have at least 2 registered players.")
                        else:
                            # Create and execute the update command
                            original_name = tournament.name  # Track the original name
                            self.update_tournament(tournament, **updates)
                            # Check if the tournament name was changed
                            if original_name != tournament.name:
                                self.remove_old_tournament_file(original_name)
                            print(f"Tournament '{tournament.name}' updated successfully.")
                            # Update the sorted list to reflect changes
                            self.sorted_tournaments = sorted(self.tournaments, key=lambda t: datetime.strptime(t.start_date, "%d-%m-%Y"),
                                                             reverse=True)
                            self.display()
                    else:
                        print("Invalid tournament number.")
                else:
                    print("Invalid tournament number.")
            elif value.upper() == 'X':
                return Context(run=False)

    def collect_tournament_updates(self, tournament):
        """Collect updates for an existing tournament."""
        updates = {}

        print(f"Enter updates for tournament '{tournament.name}' (press enter to skip):")
        for key, value in tournament.__dict__.items():
            new_value = input(f"Enter new value for {key} (current: {value}): ")
            if new_value:
                if key == 'registered_players':
                    # Ensure at least two players are entered
                    players = new_value.split(',')
                    if len(players) < 2:
                        print("A tournament must have at least 2 registered players.")
                        continue  # Skip this update if validation fails
                    updates[key] = players
                else:
                    updates[key] = new_value

        return updates

    def update_tournament(self, tournament, **kwargs):
        """Utility method to update a tournament instance based on arguments provided"""
        if tournament not in self.tournaments:
            raise RuntimeError(f"Tournament {tournament.name} not found in the list!")

        for key, value in kwargs.items():
            setattr(tournament, key, value)

        # Update the filepath after renaming
        if 'name' in kwargs:
            old_filepath = tournament.filepath
            new_filename = f"{kwargs['name'].replace(' ', '_')}.json"
            new_filepath = old_filepath.parent / new_filename
            tournament.filepath = new_filepath

        self.save_tournaments()

    def remove_old_tournament_file(self, tournament_name):
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
                print(f"No file found for the old tournament name '{file_path}' to remove.")
        except Exception as e:
            print(f"An error occurred while removing the old tournament file: {e}")

    def save_tournaments(self):
        """Save all tournaments to their respective JSON files"""
        Tournament.save_tournaments()
