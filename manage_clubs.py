from commands import TournamentListCmd, TournamentCreateCmd
from commands import ClubListCmd
from commands.context import Context
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
        # Initially, prompt the user to choose between managing clubs or tournaments
        while True:
            print("Welcome to the club management program!")
            print("Choose an option:")
            print("1. Manage Clubs")
            print("2. Manage Tournaments")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                command = ClubListCmd()
                self.context = command()
                break
            elif choice == "2":
                tournaments_folder = Path(
                    __file__).resolve().parent.parent / "P3-Application-Developer-Skills-Bootcamp" / "data" / "tournaments"

                command = TournamentListCmd(tournaments_folder)
                self.context = command()
                break
            elif choice == "3":
                print("Bye")
                self.context = False
                break
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        while self.context != False:
            # Get the screen class from the mapping
            screen = self.SCREENS[self.context.screen]
            try:
                # Run the screen and get the command
                command = screen(**self.context.kwargs).run()
                # Check if the command is a callable
                if callable(command):
                    # Run the command and get a context back
                    self.context = command()
                else:
                    # If not callable back to the main menu
                    break
            except KeyboardInterrupt:
                # Ctrl-C
                print("Bye!")
                self.context.run = False


if __name__ == "__main__":
    app = App()
    app.run()