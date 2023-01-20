from typing import Union
from controllers.manager_controller import Manager
from models.players import Player
from models.tournament import Tournament
from utils import clear_console
from colorama import Fore, Back, Style
from controllers.db_controller import Database


def view_list(
    obj_creation_controller,
    object_type,
    selection_enabled=False,
    question="",
    additional_item_create=False,
    additional_item_end=False,
    callback_condition_for_display=None,
):
    """
    View a list of objects.
    Args:
        object_type: The type of object whose list is to be viewed. Can be either a Player object or a Tournament object.
        selection_enabled: A boolean value that indicates whether to allow user to select an object from the list.
        question: A string that will be printed if selection_enabled is True, asking the user which object to select.

    Returns:
        None or the selected object
    """

    final_list = []
    initial_list = []
    if object_type == Player:
        clear_console()
        print("Liste des joueurs :")
        initial_list = Player.deserialize_players(Database.read_db("players"))
    elif object_type == Tournament:
        clear_console()
        print("Liste des tournois :")
        initial_list = Tournament.deserialize_tournament(
            Database.read_db("tournaments")
        )
    else:
        print("Entrez un Tournois ou un joueur.")
        return

    if callback_condition_for_display:
        liste = []
        print(len(initial_list))
        for object in initial_list:
            boolean = callback_condition_for_display(object)
            if boolean:
                liste.append(object)
        initial_list = liste

    # for object in initial_list:
    #     print(object.name)
    #     print(len(object.rounds), object.round_amount)

    id = 1
    for object in initial_list:
        final_list.append(object)
        Manager.view_object(object, id)
        id += 1
    if additional_item_create:
        id_as_string = str(id)
        id_as_string_plus_one = str(id + 1)
        if object_type == Player:
            print(
                Fore.CYAN
                + "-----  "
                + id_as_string
                + "  -----"
                + "\nCréer un nouveau joueur"
                + Style.RESET_ALL
            )
        elif object_type == Tournament:
            print(
                Fore.CYAN
                + "-----  "
                + id_as_string
                + "  -----"
                + "\nCréer un nouveau tournoi"
                + Style.RESET_ALL
            )
    if additional_item_end:
        id_as_string = str(id + 1)
        print(
            Fore.RED
            + "-----  "
            + id_as_string
            + "  -----"
            + "\nFin de l'ajout"
            + Style.RESET_ALL
        )
    if selection_enabled:
        selected_id = ""
        selected_id = input(question + " (Entrer 'R' pour revenir au menu principal)")
        if selected_id.upper() == "R":
            clear_console()
            return "back"
        try:
            selected_id = int(selected_id)
        except ValueError:
            print("Entrez un numéro valide ou 'R'")
            return
        if selected_id < 1 or selected_id > len(final_list) + 2:
            print("Entrez un numéro valide ")
            return
        if selected_id == len(final_list) + 1:
            obj_creation = obj_creation_controller()
            new_tournament = obj_creation.create_new()
            return new_tournament
        if selected_id == len(final_list) + 2:
            return "End"
        selected_object: Union[Player, Tournament] = final_list[selected_id - 1]
        return selected_object
    else:
        input("Appuyez sur entrée pour revenir au menu principal")
        clear_console()
