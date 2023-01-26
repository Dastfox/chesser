from models.players import Player, serialize_player
from models.tournament import Tournament, serialize_tournament
from colorama import Fore, Style
from views.lists_view import List_view


class Manager:
    def __init__(self) -> None:
        pass

    @staticmethod
    def object_list_fitting_db(
        objects: list[Player] | list[Tournament],
    ) -> list[dict]:

        list_fitting_db: list[dict] = []
        for obj in objects:
            if isinstance(obj, Player):
                list_fitting_db.append(serialize_player(obj))
            elif isinstance(obj, Tournament):
                list_fitting_db.append(serialize_tournament(obj))
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
                + "Erreur : l'objet n'est pas une"
                + " instance de Player ou de Tournament"
                + Style.RESET_ALL
            )
