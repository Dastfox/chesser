

class Tournament:
    def __init__(self, name: str, location: str, date: str,  turn: str,  time_control: str, description: str, round_amount=4, players=[]):
        self.name = name
        self.location = location
        self.date = date
        self.turn = turn
        self.time_control = time_control
        self.description = description
        self.round_amount = round_amount
        self.players = players
