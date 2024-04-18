from ..base_screen import BaseScreen

class TournamentView(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        # Display tournament information
        self.display_tournament_info()
        # Optionally, you can add more functionality here

    def display_tournament_info(self):
        # Display tournament details
        print("Tournament Information:")
        print(f"Name: {self.tournament.name}")
        # Display other tournament details
