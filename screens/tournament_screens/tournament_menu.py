from ..base_screen import BaseScreen
from commands import ExitCmd, NoopCmd



class TournamentMenu(BaseScreen):
    """Menu for tournament operations"""

    def __init__(self, tournaments):
        self.tournaments = tournaments

    def display(self):
        print("Tournaments:")
        for idx, tournament in enumerate(self.tournaments, 1):
            print(f"{idx}. {tournament.name} at {tournament.venue} from {tournament.start_date} to {tournament.end_date}")

    def get_command(self):
        while True:
            print("Type the number of a tournament to view/manage it, or 'N' to create a new tournament.")
            print("Type 'X' to exit.")
            value = self.input_string()
            if value.isdigit():
                value = int(value)
                if value in range(1, len(self.tournaments) + 1):
                    return NoopCmd("tournament-view", tournament=self.tournaments[value - 1])
            elif value.upper() == 'N':
                return NoopCmd("tournament-create")
            elif value.upper() == 'X':
                return ExitCmd()

