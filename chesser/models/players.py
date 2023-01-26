class Player:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        rank: int,
        chess_id: str,
        points: float = 0,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.chess_id = chess_id
        self.points = points

    def player_format_fitting_db(self):
        return {
            "firstname": self.first_name,
            "lastname": self.last_name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "rank": self.rank,
            "chess_id": self.chess_id,
            "points": self.points,
        }

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented

        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
        )

    @staticmethod
    def deserialize_players(player_dict_list: list[dict]):
        printable_list: list[Player] = []
        for player_dict in player_dict_list:
            if isinstance(player_dict, Player):
                printable_list.append(player_dict)
            else:
                first_name = player_dict.get("firstname", "")
                last_name = player_dict.get("lastname", "")
                birthdate = player_dict.get("birthdate", "")
                gender = player_dict.get("gender", "")
                chess_id = player_dict.get("chess_id", "")
                rank = player_dict.get("rank", 0)
                points = player_dict.get("points", 0)
                player = Player(
                    first_name,
                    last_name,
                    birthdate,
                    gender,
                    rank,
                    chess_id,
                    points,
                )
                printable_list.append(player)
        for player in printable_list:
            if not isinstance(player, Player):
                raise ValueError(
                    "The list should only contain Player objects."
                )
        return printable_list


def serialize_players(players: list[Player]) -> list[dict]:
    player_list = []
    for player in players:
        player_serialized = {
            "firstname": player.first_name,
            "lastname": player.last_name,
            "birthdate": player.birthdate,
            "gender": player.gender,
            "rank": player.rank,
            "chess_id": player.chess_id,
            "points": player.points,
        }
        player_list.append(player_serialized)
    return player_list


def serialize_player(player: Player) -> dict:
    player_serialized = {
        "firstname": player.first_name,
        "lastname": player.last_name,
        "birthdate": player.birthdate,
        "gender": player.gender,
        "rank": player.rank,
        "chess_id": player.chess_id,
        "points": player.points,
    }
    return player_serialized
