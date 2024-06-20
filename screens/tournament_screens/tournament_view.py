from ..base_screen import BaseScreen
from commands.context import Context
from commands import NoopCmd, TournamentListCmd
from commands import NoopCmd, ClubListCmd
from models import ClubManager
from models import Tournament
from screens.tournament_screens import TournamentMenu
from models.tournament import PlayerDetails
from commands.exit import ExitCmd
from pathlib import Path

class TournamentView(BaseScreen):
    def __init__(self, tournament, clubs=None, tournaments_folder=None, tournaments=None):
        self.tournament = tournament
        self.tournaments = tournaments
        self.clubs = clubs
        self.tournaments_folder = tournaments_folder

    def run(self):
        self.display_tournament_info()
        return self.get_command()

    def display_tournament_info(self):
        print("Tournament Information:")
        print(f"Name: {self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"Number of Rounds: {self.tournament.num_rounds}")
        print(f"Current Round: {self.tournament.current_round}")
        print("List of Players:")

        for player_info in self.tournament.registered_players:
            if isinstance(player_info, str):
                print(f"Player ID/Name: {player_info}")
            elif isinstance(player_info, PlayerDetails):
                print(f"Player Name: {player_info.name}")
                # Add other attributes like email, chess_id, birthday if needed
                print(f"Email: {player_info.email}")
                print(f"Chess ID: {player_info.chess_id}")
                print(f"Birthday: {player_info.birthday}")
            elif isinstance(player_info, dict):
                # Convert dictionary to PlayerDetails if it's supposed to represent one
                player_details = PlayerDetails(**player_info)
                print(f"Player Name: {player_details.name}")
                # Add other attributes like email, chess_id, birthday if needed
                print(f"Email: {player_details.email}")
                print(f"Chess ID: {player_details.chess_id}")
                print(f"Birthday: {player_details.birthday}")
            else:
                print(f"Unknown player information format: {type(player_info)}")

    def get_command(self):
        while True:
            print("Type 'B' to go back to main menu or Type 'CR' to enter results for current round")
            action = input("Enter your action: ").strip().upper()
            if action == "B":
                folder_path = Path("E:\\GitProjects\\P3-Application-Developer-Skills-Bootcamp\\data\\tournaments")
                return TournamentListCmd(folder_path)
            elif action =="CR":
                return
            elif action == "X":
                return NoopCmd("exit", clubs=False)
            else:
                print("Invalid action. Please try again.")
