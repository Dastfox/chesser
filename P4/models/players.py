import re


class Player:
    def __init__(
        self, first_name: str, last_name: str, birthdate: str, gender: str, rank: int
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank

    def player_format_fitting_db(self):
        return {
            "firstname": self.first_name,
            "lastname": self.last_name,
            "birthdate": self.birthdate,
            "genre": self.gender,
            "rank": self.rank,
        }

    def player_format_fitting_python(player_dict_list: list[dict]):
        printable_list = []
        for player_dict in player_dict_list:
            fistName, lastName, birthdate, gender, rank = player_dict.values()
            unserialized_player = Player(fistName, lastName, birthdate, gender, rank)
            printable_list.append(unserialized_player)
        return printable_list
