import random
from views.lists_view import List_view

# from views.lists_view import List_view
from models.round import Round, serialize_round, deserialize_round
from models.players import Player, serialize_players
import random
from datetime import datetime
from typing import List, Tuple, Union
from models.players import Player
from models.round import Round


class Tournament:
    def __init__(
        self,
        name: str,
        location: str,
        date: str,
        round_amount: int,
        round: list[Round],
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
        self.round = round
        self.players = players
        self.time_control = time_control
        self.description = description
        self.pair_played = pair_played
        self.leaderboard = leaderboard

    @staticmethod
    def deserialize_tournament(tournament_data_list: list[dict]):
        tournament_list = []
        for tournament_data in tournament_data_list:
            players = Player.deserialize_players(tournament_data["players"])
            round = deserialize_round(tournament_data["round"])
            tournament_list.append(
                Tournament(
                    name=tournament_data["name"],
                    location=tournament_data["location"],
                    date=tournament_data["date"],
                    round_amount=tournament_data["round_amount"],
                    round=round,
                    players=players,
                    time_control=tournament_data["time_control"],
                    description=tournament_data["description"],
                    pair_played=tournament_data["pair_played"],
                    leaderboard=tournament_data["leaderboard"],
                )
            )
        return tournament_list

    def generate_pairs(self):
        if self.round == None:
            self.round = []
        round_num = len(self.round) + 1
        self.round.append(
            Round(
                id=f"Round {round_num}",
                is_finished=False,
                date_time_start=str(datetime.now()),
                date_time_end="",
                matches=[],
            )
        )
        random.shuffle(self.players)
        self.players.sort(key=lambda x: x.points, reverse=True)
        pairs = [
            (self.players[i], self.players[i + 1])
            for i in range(0, len(self.players) - 1, 2)
        ]
        for p1, p2 in pairs:
            if (p1, p2) not in self.pair_played and (p2, p1) not in self.pair_played:
                self.round[-1].matches.append((p1, p2, None))
                self.pair_played.append((p1, p2))
            else:
                available_players = [
                    p
                    for p in self.players
                    if p not in (p1, p2)
                    and (p, p1) not in self.pair_played
                    and (p, p2) not in self.pair_played
                ]
                if available_players:
                    p2 = random.choice(available_players)
                    self.round[-1].matches.append((p1, p2, None))
                    self.pair_played.append((p1, p2))
        self.update_points()
        if self.round[-1]:
            return self.round[-1]

    def update_points(self):
        for p1, p2, result in self.round[-1].matches:
            if result == 1:
                p1.points += 1
            elif result == 2:
                p2.points += 1
            elif result == "D":
                p1.points += 0.5
                p2.points += 0.5

    def play_match(self, match_idx: int, result: Union[int, str]):
        p1, p2, _ = self.round[-1].matches[match_idx]
        self.round[-1].matches[match_idx] = (p1, p2, result)

    def play_round(self):
        print(f"Playing round {self.round[-1].id}")
        for idx, (p1, p2, result) in enumerate(self.round[-1].matches):
            j1 = Player.deserialize_players([p1])[0]
            j2 = Player.deserialize_players([p2])[0]
            print(f"Playing match {idx + 1}")
            List_view.view_match((j1, j2, None))
            result = input(
                "Enter match result (1 for player 1, 2 for player 2, D for draw): "
            )
            while result not in ("1", "2", "D", "d"):
                result = input(
                    "Enter match result (1 for player 1, 2 for player 2, D for draw): "
                )
            self.play_match(idx, result)


def serialize_tournament(tournament: Tournament):

    rounds = serialize_round(tournament.round)
    players = serialize_players(tournament.players)
    pair_played = []
    for pair in tournament.pair_played:
        if isinstance(pair[0], Player) and isinstance(pair[1], Player):
            pair_played.append(
                (serialize_players([pair[0]])[0], serialize_players([pair[1]])[0])
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
