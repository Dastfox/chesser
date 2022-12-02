from models.players import Player
from models.tournament import Tournament
import os

class Manager:
    def __init__(self) -> None:
        pass

    def player_list_fiting_db(players: list[Player]):
        print ("player_list_fittin_db",players)
        list_fitting_db = []
        for player in players:
            list_fitting_db.append(player.format_fiting_db())
        return list_fitting_db

    def view_all_players(self):
        pass

    def create_new_tournament(self):
        new_tournament = Tournament()
        pass

    def view_tournament(self):
        pass

    def play_tournament(self, tournament:Tournament):
        pass

