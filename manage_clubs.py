
from commands import ClubListCmd
from screens import ClubCreate, ClubView, MainMenu, PlayerEdit, PlayerView

# Inside manage_clubs.py
from tournament_commands.tournament_list_cmd import TournamentListCmd
from tournament_commands.tournament_create_cmd import TournamentCreateCmd
from screens.tournament_screens import TournamentView, TournamentMenu

class App:
    """The main controller for the club management program"""

    SCREENS = {
        "main-menu": MainMenu,
        "club-create": ClubCreate,
        "club-view": ClubView,
        "player-view": PlayerView,
        "player-edit": PlayerEdit,
        "player-create": PlayerEdit,
        "tournament-menu": TournamentMenu,  # Adjust screen mapping for tournament menu
        "tournament-create": TournamentCreateCmd,
        "tournament-view": TournamentView,
        "exit": False,
    }

    def __init__(self):
        # Start with the main menu
        self.context = {"screen": "main-menu", "run": True}

    def run(self):
        while self.context["run"]:
            screen_name = self.context["screen"]
            if screen_name == "main-menu":
                command = ClubListCmd()
                self.context = command()
            elif screen_name == "tournament-menu":
                command = TournamentListCmd()
                self.context = command()

            # Get the screen class from the mapping
            screen_class = self.SCREENS[screen_name]
            try:
                # Run the screen and get the command
                command = screen_class(**self.context).run()
                # Run the command and get a context back
                self.context = command()
            except KeyboardInterrupt:
                # Ctrl-C
                print("Bye!")
                self.context["run"] = False

if __name__ == "__main__":
    app = App()
    app.run()
