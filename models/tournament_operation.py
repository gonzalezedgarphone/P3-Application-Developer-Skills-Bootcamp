from typing import List, Tuple, Union
import random
from models.tournament import Tournament, PlayerDetails

PlayerType = Union[PlayerDetails, dict]


class TournamentOperations:
    @staticmethod
    def generate_pairings_from_tournament(
        tournament: Tournament, previous_pairings: set = None
    ) -> List[Tuple[PlayerType, PlayerType]]:
        if previous_pairings is None:
            previous_pairings = set()

        return TournamentOperations.generate_swiss_pairings(
            tournament.registered_players, previous_pairings
        )

    @staticmethod
    def generate_swiss_pairings(
        players: List[PlayerType], previous_pairings: set = None
    ) -> List[Tuple[PlayerType, PlayerType]]:
        if previous_pairings is None:
            previous_pairings = set()

        # Sort players by points
        players.sort(
            key=lambda player: (
                player.points if isinstance(player, PlayerDetails) else player["points"]
            ),
            reverse=True,
        )

        paired_players = []
        paired_ids = set()

        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1] if i + 1 < len(players) else None

            player1_id = (
                player1.chess_id
                if isinstance(player1, PlayerDetails)
                else player1["chess_id"]
            )
            player2_id = (
                player2.chess_id
                if player2 and isinstance(player2, PlayerDetails)
                else player2["chess_id"] if player2 else None
            )

            if (
                player1
                and player2
                and (player1_id, player2_id) not in previous_pairings
                and (player2_id, player1_id) not in previous_pairings
            ):
                paired_players.append((player1, player2))
                paired_ids.add(player1_id)
                paired_ids.add(player2_id)
                # Add this pairing to previous pairings to avoid future repeats
                previous_pairings.add((player1_id, player2_id))
            elif player2 is None:
                paired_players.append((player1, None))

        return paired_players

    @staticmethod
    def play_round(
        pairings: List[Tuple[PlayerType, PlayerType]]
    ) -> List[Tuple[PlayerType, PlayerType, str]]:
        results = []

        for player1, player2 in pairings:
            if player2 is None:
                if isinstance(player1, PlayerDetails):
                    player1.points += 1
                else:
                    player1["points"] += 1
                results.append((player1, None, "bye"))
            else:
                result = random.choice(["win", "draw", "loss"])

                if result == "win":
                    if isinstance(player1, PlayerDetails):
                        player1.points += 1
                    else:
                        player1["points"] += 1
                elif result == "draw":
                    if isinstance(player1, PlayerDetails):
                        player1.points += 0.5
                        player2.points += 0.5
                    else:
                        player1["points"] += 0.5
                        player2["points"] += 0.5
                elif result == "loss":
                    if isinstance(player2, PlayerDetails):
                        player2.points += 1
                    else:
                        player2["points"] += 1

                results.append((player1, player2, result))

        return results

    @staticmethod
    def sort_players(players: List[PlayerType]) -> List[PlayerType]:
        return sorted(
            players,
            key=lambda player: (
                player.points if isinstance(player, PlayerDetails) else player["points"]
            ),
            reverse=True,
        )

    @staticmethod
    def print_rankings(players: List[PlayerType]):
        print("Rankings:")
        for i, player in enumerate(players, 1):
            points = (
                player.points if isinstance(player, PlayerDetails) else player["points"]
            )
            print(
                f"{i}. {player.name if isinstance(player, PlayerDetails) else player['name']}: {points} points"
            )
        print("********************")
        print()
