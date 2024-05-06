from commands.tournament_commands import TournamentListCmd, TournamentCreateCmd
from commands import ClubListCmd
from screens import ClubCreate, ClubView, MainMenu, PlayerEdit, PlayerView, TournamentView, TournamentMenu
from pathlib import Path
class App:
    """The main controller for the club management program"""

    SCREENS = {
        "main-menu": MainMenu,
        "club-create": ClubCreate,
        "club-view": ClubView,
        "player-view": PlayerView,
        "player-edit": PlayerEdit,
        "player-create": PlayerEdit,
        "tournament-menu": TournamentMenu,
        "tournament-create": TournamentCreateCmd,
        "tournament-view": TournamentView,
        "exit": False,
    }

    def __init__(self):
        # Initialize commands to load club and tournament lists
        club_command = ClubListCmd()
        tournaments_folder = Path(__file__).resolve().parent.parent/"P3-Application-Developer-Skills-Bootcamp" / "data" / "tournaments"
        tournament_command = TournamentListCmd(tournaments_folder)

        # Execute commands to get initial contexts
        self.club_context = club_command()
        self.tournament_context = tournament_command()

        # Initialize current context as None
        self.context = None

    def run(self):
        while not self.context or self.context.get("run", False):
            if not self.context:
                self.choose_list()

            screen_name = self.context.screen  # Use dot notation to access attributes
            screen_class = self.SCREENS[screen_name]

            try:
                command = screen_class(**self.context.kwargs).run()
                self.context = command()
            except KeyboardInterrupt:
                print("Bye!")
                if self.context:
                    self.context.run = False
                else:
                    break

    def choose_list(self):
        print("Welcome to the club management program!")
        print("Choose an option:")
        print("1. Manage Clubs")
        print("2. Manage Tournaments")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.context = self.club_context
        elif choice == "2":
            self.context = self.tournament_context
        elif choice == "3":
            self.context = {"screen": "exit", "run": False}
        else:
            print("Invalid choice. Please try again.")
            self.choose_list()


if __name__ == "__main__":
    app = App()
    app.run()