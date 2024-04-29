from ..base_screen import BaseScreen
class TournamentView(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        self.display_tournament_info()
        # Handle the tournament logic here (e.g., managing rounds)

    def display_tournament_info(self):
        print("Tournament Information:")
        print(f"Name: {self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        # Add more details and options for matches, rounds etc.
