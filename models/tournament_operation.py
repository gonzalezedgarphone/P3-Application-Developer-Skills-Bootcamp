# tournament_utils.py

import random
from typing import List, Tuple
from player import Player


class TournamentOperations:
    @staticmethod
    def generate_swiss_pairings(players: List[Player], previous_pairings: set = None) -> List[Tuple[Player, Player]]:
        if previous_pairings is None:
            previous_pairings = set()

        # Sort players based on their points
        players.sort(key=lambda x: x.points, reverse=True)

        # Generate pairings
        pairings = []
        matched_players = set()

        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1] if i + 1 < len(players) else None

            # Check if this pair has already played together
            if player2 is not None and ((player1.name, player2.name) in previous_pairings or
                                         (player2.name, player1.name) in previous_pairings):
                # Find a different opponent for player1
                for j in range(i + 2, len(players)):
                    opponent = players[j]
                    if ((player1.name, opponent.name) not in previous_pairings and
                            (opponent.name, player1.name) not in previous_pairings):
                        player2 = opponent
                        break

            if player2 is not None:
                # Add the pair to the list of valid pairings
                pairings.append((player1, player2))
                matched_players.add(player1)
                matched_players.add(player2)

                # Update previous pairings
                previous_pairings.add((player1.name, player2.name))

        # Handle unpaired players
        unpaired_players = [player for player in players if player not in matched_players]
        for player in unpaired_players:
            pairings.append((player, None))

        return pairings

    @staticmethod
    def play_round(pairings: List[Tuple[Player, Player]]) -> List[Tuple[Player, Player, str]]:
        results = []
        for player1, player2 in pairings:
            if player2 is None:
                player1.points += 1
                results.append((player1, None, "bye"))
            else:
                result = random.choice(["win", "draw", "loss"])
                if result == "win":
                    player1.points += 1
                elif result == "draw":
                    player1.points += 0.5
                    player2.points += 0.5
                elif result == "loss":
                    player2.points += 1
                    player1.points += 0
                results.append((player1, player2, result))
        return results

    @staticmethod
    def sort_players(players: List[Player]) -> List[Player]:
        return sorted(players, key=lambda x: x.points, reverse=True)

    @staticmethod
    def print_rankings(players: List[Player]):
        print("Rankings:")
        for i, player in enumerate(players, 1):
            print(f"{i}. {player.name}: {player.points} points : player id {player.chess_id}")
