from ..base_screen import BaseScreen
from pathlib import Path
from models.tournament import PlayerDetails
from commands import TournamentListCmd, NoopCmd
from models import TournamentOperations


class TournamentView(BaseScreen):
    def __init__(
        self, tournament, clubs=None, tournaments_folder=None, tournaments=None
    ):
        self.tournament = tournament
        self.tournaments = tournaments
        self.clubs = clubs
        self.tournaments_folder = tournaments_folder

        # Generate pairings for the first round
        self.first_round_pairings = (
            TournamentOperations.generate_pairings_from_tournament(self.tournament)
        )
        self.tournament.rounds = [[] for _ in range(self.tournament.num_rounds)]
        self.tournament.rounds[0] = [
            {
                "players": (
                    [player1.chess_id, player2.chess_id]
                    if player2
                    else [player1.chess_id]
                ),
                "completed": False,
            }
            for player1, player2 in self.first_round_pairings
        ]
        # Print pairings for verification only if the current round is 1
        if self.tournament.current_round == 1:
            print("First Round Pairings:")
            print("=====================")
            for player1, player2 in self.first_round_pairings:
                if player2:
                    print(f"{player1.name} vs {player2.name}")
                else:
                    print(f"{player1.name} (Bye)")
            print("=====================")

    def run(self):
        while True:
            self.display_tournament_info_without_players()
            command = self.get_command()
            if command:
                return command

    def display_tournament_info(self):
        print("--------------------")
        print("Tournament Information:")
        print(f"Name: {self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"Number of Rounds: {self.tournament.num_rounds}")
        print(f"Current Round: {self.tournament.current_round}")
        print()
        print("The List of Current Players in Tournament")
        print("Players Information:")
        print("--------------------")

        for player_info in self.tournament.registered_players:
            details = []

            if isinstance(player_info, PlayerDetails):
                if player_info.name:
                    details.append(f"Player Name: {player_info.name}")
                if player_info.email:
                    details.append(f"Email: {player_info.email}")
                if player_info.chess_id:
                    details.append(f"Play ID: {player_info.chess_id}")
                if player_info.birthday:
                    details.append(f"Birthday: {player_info.birthday}")
            elif isinstance(player_info, dict):
                player_details = PlayerDetails(**player_info)
                if player_details.name:
                    details.append(f"Player Name: {player_details.name}")
                if player_details.email:
                    details.append(f"Email: {player_details.email}")
                if player_details.chess_id:
                    details.append(f"Play ID: {player_details.chess_id}")
                if player_details.birthday:
                    details.append(f"Birthday: {player_details.birthday}")
            else:
                print(f"Unknown player information format: {type(player_info)}")
                continue

            if details:
                print(": ".join(details))
        print("********************")

    def get_command(self):
        print(
            "Type 'B' to go back to main menu, 'CR' to enter results for current round, or 'R' to generate report"
        )
        action = input("Enter your action: ").strip().upper()
        if action == "B":
            folder_path = Path(
                "E:\\GitProjects\\P3-Application-Developer-Skills-Bootcamp\\data\\tournaments"
            )
            return TournamentListCmd(folder_path)
        elif action == "CR":
            self.enter_results_for_current_round()
        elif action == "AR":
            self.advance_to_next_round()
        elif action == "R":
            self.generate_tournament_report()
        elif action == "E":
            return NoopCmd("exit", clubs=False)
        else:
            print("Invalid action. Please try again.")

    def enter_results_for_current_round(self):
        if self.tournament.finished:
            print("Tournament is already finished. Cannot enter results.")
            return

        if self.tournament.current_round == 0:
            self.tournament.current_round = 1

        if not self.tournament.rounds[self.tournament.current_round - 1]:
            pairings = TournamentOperations.generate_pairings_from_tournament(
                self.tournament
            )
            self.tournament.rounds[self.tournament.current_round - 1] = [
                {"players": [player1.chess_id, player2.chess_id], "completed": False}
                for player1, player2 in pairings
            ]

        round_results = self.tournament.rounds[self.tournament.current_round - 1]

        for match in round_results:
            player1_id, player2_id = match["players"]
            player1 = next(
                (
                    p
                    for p in self.tournament.registered_players
                    if p.chess_id == player1_id
                ),
                None,
            )
            player2 = next(
                (
                    p
                    for p in self.tournament.registered_players
                    if p.chess_id == player2_id
                ),
                None,
            )

            if not match.get("completed", False):
                player1_name = player1.name if player1.name else player1.chess_id
                player2_name = (
                    player2.name
                    if player2 and player2.name
                    else player2.chess_id if player2 else "Bye"
                )

                result = (
                    input(
                        f"Result for {player1_name} vs {player2_name} (win/draw/loss): "
                    )
                    .strip()
                    .lower()
                )
                while result not in ["win", "draw", "loss"]:
                    print("Invalid result. Please enter 'win', 'draw', or 'loss'.")
                    result = (
                        input(
                            f"Result for {player1_name} vs {player2_name} (win/draw/loss): "
                        )
                        .strip()
                        .lower()
                    )

                match["completed"] = True
                if result == "win":
                    match["winner"] = player1_id
                    player1.points += 1
                    print(f"{player1_name} wins against {player2_name}")
                elif result == "draw":
                    match["winner"] = None
                    player1.points += 0.5
                    if player2:
                        player2.points += 0.5
                    print(f"{player1_name} and {player2_name} draw")
                elif result == "loss":
                    match["winner"] = player2_id
                    if player2:
                        player2.points += 1
                    print(f"{player2_name} wins against {player1_name}")

        self.tournament.save()
        self.advance_to_next_round()

    def advance_to_next_round(self):
        if self.tournament.finished:
            print("Tournament is already finished.")
            return

        if self.tournament.current_round >= self.tournament.num_rounds:
            self.tournament.finished = True
            print(
                "Tournament has reached the maximum number of rounds and is now finished."
            )
        else:
            confirmation = (
                input("Are you sure you want to advance to the next round? (yes/no): ")
                .strip()
                .lower()
            )
            if confirmation == "yes":
                self.tournament.current_round += 1
                print(f"Advancing to Round {self.tournament.current_round}")
                self.tournament.save()
            elif confirmation == "no":
                print("Operation cancelled.")
            else:
                print("Invalid input. Operation cancelled.")

    def generate_tournament_report(self):
        print(f"Tournament Report for {self.tournament.name}")
        self.display_tournament_info()
        players = self.tournament.registered_players
        sorted_players = TournamentOperations.sort_players(players)
        TournamentOperations.print_rankings(sorted_players)

        for i, round_results in enumerate(self.tournament.rounds, start=1):
            print("--------------------")
            print(f"\nRound {i} Results: ")
            for match in round_results:
                player1_id, player2_id = match["players"]
                result = match.get("winner")

                player1 = next((p for p in players if p.chess_id == player1_id), None)
                player2 = next((p for p in players if p.chess_id == player2_id), None)

                if player1 and player2:
                    if result == player1_id:
                        match_result = f"{player1.name} wins"
                    elif result == player2_id:
                        match_result = f"{player2.name} wins"
                    else:
                        match_result = "Draw"

                    print(f"{player1.name} vs {player2.name}: {match_result}")
                elif player1 and not player2:
                    print(f"{player1.name} (Bye)")
                else:
                    print("Invalid match data. Could not find players.")
        # self.display_tournament_info()
        print("--------------------")

    def display_tournament_info_without_players(self):
        print("Tournament Information:")
        print(f"Name: {self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"Number of Rounds: {self.tournament.num_rounds}")
        print(f"Current Round: {self.tournament.current_round}")
