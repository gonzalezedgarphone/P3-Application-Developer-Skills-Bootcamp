from models.tournament import Tournament
from models.player import Player

class TournamentCreateCmd(Tournament):
    def __init__(self, venue, start_date, end_date, num_rounds, current_round, name, registered_players):
        super().__init__(name, venue, start_date, end_date, registered_players, num_rounds, current_round)
        self.email = None  # Initialize these attributes as None or as needed
        self.chess_id = None
        self.birthday = None

    def questions(self):
        self.name = input("Enter tournament name: ")
        self.venue = input("Enter tournament venue: ")
        self.start_date = input("Enter tournament start date (DD-MM-YYYY): ")
        self.end_date = input("Enter tournament end date (DD-MM-YYYY): ")
        self.num_rounds = int(input("Enter number of rounds: "))
        self.current_round = int(input("Enter current round: "))

        self.registered_players = []  # Initialize the list of registered players

        # Prompt for player information and add them to the list
        while True:
            name = input("Enter player name: ")
            chess_id = input("Enter player chess ID: ")
            player = Player(name=name, chess_id=chess_id)
            self.registered_players.append(player)

            add_another = input("Add another player? (yes/no): ")
            if add_another.lower() != "yes":
                break

        print(f"Tournament '{self.name}' created successfully.")

    def to_dict(self):
        players_data = []
        for player in self.registered_players:
            players_data.append({
                "name": player.name,
                "chess_id": player.chess_id,
                # Add more attributes as needed
            })

        return {
            "name": self.name,
            "venue": self.venue,
            "dates": {"from": self.start_date, "to": self.end_date},
            "players": players_data,
            "number_of_rounds": self.num_rounds,
            "current_round": self.current_round,
            "completed": self.completed,  # Ensure these attributes are defined in your class
            "finished": self.finished,
            "rounds": self.rounds
        }
