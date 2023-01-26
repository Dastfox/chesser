import random
from views.object_view import Object_view
from models.round import Round, serialize_round, deserialize_round
from models.players import Player, serialize_players
from datetime import datetime
from typing import Union


class Tournament:
    def __init__(
        self,
        name: str,
        location: str,
        date: str,
        round_amount: int,
        rounds: list[Round],
        players: list[Player],
        time_control: str,
        description: str,
        pair_played: list = [],
        leaderboard: list = [],
    ):
        self.name = name
        self.location = location
        self.date = date
        self.round_amount = round_amount
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description
        self.pair_played = pair_played
        self.leaderboard = leaderboard

    @staticmethod
    def deserialize_tournament(tournament_data_list: list[dict]):
        tournament_list: list[Tournament] = []
        for tournament_data in tournament_data_list:
            players = Player.deserialize_players(tournament_data["players"])
            round = deserialize_round(tournament_data["round"])
            tournament_list.append(
                Tournament(
                    name=tournament_data["name"],
                    location=tournament_data["location"],
                    date=tournament_data["date"],
                    round_amount=tournament_data["round_amount"],
                    rounds=round,
                    players=players,
                    time_control=tournament_data["time_control"],
                    description=tournament_data["description"],
                    pair_played=tournament_data["pair_played"],
                    leaderboard=tournament_data["leaderboard"],
                )
            )
        return tournament_list

    def generate_pairs(self):
        """

        This method is used to generate pairs of players for the next
        round of a tournament. It shuffles and sorts the players in
        the tournament by their points, and then pairs the players up.
        If a pair of players has already played each other in a
        previous round, it will randomly choose another player
        for one of the members of the pair to play against.

        Example:

        tournament = Tournament()

        tournament.players = [
            Player("John", "Doe", "1"),
            Player("Jane", "Doe", "2"),
            Player("Bob", "Smith", "3")
        ]

        tournament.generate_pairs()

        This will generate a new round for the tournament
        with the players John Doe, Jane Doe, and Bob Smith
        paired up in matches.
        """
        if self.rounds is None:
            self.rounds = []
        round_num = len(self.rounds) + 1
        self.rounds.append(
            Round(
                id=f"Round {round_num}",
                is_finished=False,
                date_time_start=str(datetime.now()),
                date_time_end="",
                matches=[],
            )
        )
        if len(self.players) == 2:
            self.rounds[-1].matches.append(
                (self.players[0], self.players[1], None)
            )
            return self.rounds[-1]
        random.shuffle(self.players)
        self.players.sort(key=lambda x: x.points, reverse=True)
        pairs = [
            (self.players[i], self.players[i + 1])
            for i in range(0, len(self.players) - 1, 2)
        ]
        for p1, p2 in pairs:
            if (p1, p2) not in self.pair_played and (
                p2,
                p1,
            ) not in self.pair_played:
                self.rounds[-1].matches.append((p1, p2, None))
                self.pair_played.append((p1, p2))
            else:
                available_players = [
                    p for p in self.players if p not in (p1, p2)
                ]
                least_played = min(
                    [
                        (
                            p,
                            self.pair_played.count((p, p1))
                            + self.pair_played.count((p1, p)),
                        )
                        for p in available_players
                    ],
                    key=lambda x: x[1],
                )[0]
                self.rounds[-1].matches.append((p1, least_played, None))
                self.pair_played.append((p1, least_played))

        return self.rounds[-1]

    def update_points(self):
        current_round = self.rounds[-1]
        for match in current_round.matches:
            p1: Player = Player.deserialize_players([match[0]])[0]
            player1 = next(player for player in self.players if player == p1)
            p2: Player = Player.deserialize_players([match[1]])[0]
            player2 = next(player for player in self.players if player == p2)
            result = match[2]
            if result == "1" or result == "2":
                result = int(result)

            if result == 1:
                p1.points += 1
            elif result == 2:
                p2.points += 1
            elif result == "D" or result == "d":
                p1.points += 0.5
                p2.points += 0.5
            player1.points = p1.points
            player2.points = p2.points

    def play_round(self):
        current_round = self.rounds[-1]
        Object_view.view_play_round(current_round.id)

        for idx, (p1, p2, result) in enumerate(current_round.matches):
            if result is not None:
                continue
            j1 = Player.deserialize_players([p1])[0]
            j2 = Player.deserialize_players([p2])[0]
            print(f"Match {idx + 1}")
            Object_view.view_match((j1, j2, None))
            result = input("Résultat du match ? : ")
            while result not in ("1", "2", "D", "d", "R", "r"):
                result = input("Résultat du match ? : ")
                if result in ("R", "r"):
                    break
            play_match(current_round, idx, result)
        if current_round.matches[-1][2] is not None:
            current_round.is_finished = True
            current_round.date_time_end = str(datetime.now())
        self.update_points()

    def update_ranks(self):
        self.players.sort(key=lambda x: x.points, reverse=False)
        for idx, player in enumerate(self.players):
            player.rank = idx + 1


def serialize_tournament(tournament: Tournament):
    if not tournament.rounds:
        rounds = []
    elif isinstance(tournament.rounds[0], Round):
        rounds = serialize_round(tournament.rounds)
    else:
        rounds = tournament.rounds

    if (tournament.players is None) or (tournament.players == []):
        players = []
    elif isinstance(tournament.players[0], Player):
        players = serialize_players(tournament.players)
    else:
        players = tournament.players

    pair_played = []
    for pair in tournament.pair_played:
        if isinstance(pair[0], Player) and isinstance(pair[1], Player):
            pair_played.append(
                (
                    serialize_players([pair[0]])[0],
                    serialize_players([pair[1]])[0],
                )
            )
        else:
            pair_played.append(pair)
    return {
        "name": tournament.name,
        "location": tournament.location,
        "date": tournament.date,
        "round_amount": tournament.round_amount,
        "round": rounds,
        "players": players,
        "time_control": tournament.time_control,
        "description": tournament.description,
        "pair_played": pair_played,
        "leaderboard": tournament.leaderboard,
    }


def play_match(current_round: Round, match_idx: int, result: Union[int, str]):
    p1, p2, _ = current_round.matches[match_idx]
    if result in ("R", "r"):
        return current_round
    if result in ("1", "2"):
        current_round.matches[match_idx] = (p1, p2, result)
    elif result in ("D", "d"):
        current_round.matches[match_idx] = (p1, p2, "D")
    else:
        raise ValueError("Invalid match result.")
