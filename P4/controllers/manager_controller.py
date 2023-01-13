from models.players import Player
from models.tournament import Tournament
import os
from colorama import Fore, Style
from views.lists_view import List_view


class Manager:
    def __init__(self) -> None:
        pass

    @staticmethod
    def object_list_fitting_db(objects: list):
        list_fitting_db = []
        for obj in objects:
            if isinstance(obj, Player):
                list_fitting_db.append(obj.player_format_fitting_db())
            elif isinstance(obj, Tournament):
                list_fitting_db.append(obj.tournament_format_fitting_db())
        return list_fitting_db
    """
    Display list of objects
    """

    @staticmethod
    def view_object(object, id: int = 0):
        if isinstance(object, Player):
            List_view.view_player(object, id)
        elif isinstance(object, Tournament):
            List_view.view_tournament(object, id)
        else:
            print(
                Fore.RED
                + "Erreur : l'objet n'est pas une instance de Player ou de Tournament"
                + Style.RESET_ALL
            )

    def add_player_to_tournament(self, player: Player, tournament: Tournament) -> None:
        """
        Adds a player to a tournament.

        Parameters:
        player (Player): The player object to add to the tournament.
        tournament (Tournament): The tournament object to add the player to.

        Returns:
        None
        """
        if player not in tournament.players:
            tournament.players.append(player)
            print(
                f"Le joueur {player.first_name} {player.last_name} a été ajouté au tournoi {tournament.name}."
            )
        else:
            print(
                f"Le joueur {player.first_name} {player.last_name} est déjà présent dans le tournoi {tournament.name}."
            )
