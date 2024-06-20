from commands.base import BaseCommand
from commands.context import Context
from models import Tournament

class TournamentListCmd(BaseCommand):
    """
    Command to list all tournaments.
    """

    def __init__(self, tournaments_folder):
        self.tournaments_folder = tournaments_folder

    def execute(self):
        # Load tournaments from the specified folder
        tournaments = Tournament.load_tournaments_from_folder(self.tournaments_folder)
        # Return a Context object with the loaded tournaments and screen name
        return Context(screen="tournament-menu", tournaments=tournaments)
