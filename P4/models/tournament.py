from models.players import Player


class Tournament:
    def __init__(
        self,
        name: str,
        location: str,
        date: str,
        round_amount: int,
        turn: dict,
        players: list[Player],
        time_control: str,
        description: str,
    ):
        self.name = name
        self.location = location
        self.date = date
        self.round_amount = round_amount
        self.turn = turn
        self.players = players
        self.time_control = time_control
        self.description = description

    def tournament_format_fitting_db(self):
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "round_amount": self.round_amount,
            "turn": self.turn,
            "players": self.players,
            "time_control": self.time_control,
            "description": self.description,
        }

    @staticmethod
    def tournament_format_fitting_python(tournament_dict_list: list[dict]):
        printable_list = []
        for tournament_dict in tournament_dict_list:
            (
                name,
                location,
                date,
                round_amount,
                turn,
                players,
                time_control,
                description,
            ) = tournament_dict.values()
            unserialized_tournament = Tournament(
                name,
                location,
                date,
                round_amount,
                turn,
                players,
                time_control,
                description,
            )
            printable_list.append(unserialized_tournament)
        return printable_list
