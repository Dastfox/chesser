

class Player:
    def __init__(self,first_name: str, last_name: str, birthdate: str,  gender: str,rank: int):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        # gender, bdate, Lname, Fname

    def format_fiting_db(self):
        return {"firstname": self.first_name, "lastname": self.last_name, "birthdate": self.birthdate, "genre": self.gender, "rank": self.rank}
