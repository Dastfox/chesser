from models.players import Player, serialize_players


class Round:
    def __init__(
        self,
        id: str,
        is_finished: bool,
        date_time_start: str = "",
        date_time_end: str = "",
        matches: list = [],
    ):
        self.id = id
        self.is_finished = is_finished
        self.date_time_start = date_time_start
        self.date_time_end = date_time_end
        self.matches = matches


def serialize_round(round_list: list[Round]):

    round_data_list = []
    for round in round_list:
        match_data_list = []
        for match in round.matches:
            if isinstance(match[0], Player) and isinstance(match[1], Player):
                serialized_match = [
                    serialize_players([match[0]])[0],
                    serialize_players([match[1]])[0],
                    match[2],
                ]
                match_data_list.append(serialized_match)
            else:
                match_data_list.append(match)
        if not isinstance(round, Round):
            return None
        else:
            round_data = {
                "id": round.id,
                "is_finished": round.is_finished,
                "date_time_start": round.date_time_start,
                "date_time_end": round.date_time_end,
                "matches": match_data_list,
            }
            round_data_list.append(round_data)
    return round_data_list


def deserialize_round(round_data_list: list[dict]):
    round_list: list[Round] = []
    for round_data in round_data_list:
        round_list.append(
            Round(
                id=round_data["id"],
                is_finished=round_data["is_finished"],
                date_time_start=round_data["date_time_start"],
                date_time_end=round_data["date_time_end"],
                matches=round_data["matches"],
            )
        )
    return round_list
