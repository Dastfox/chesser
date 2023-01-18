from typing import Union
from models.players import Player
from models.tournament import Tournament
from utils import clear_console
from colorama import Fore, Back, Style


def view_list(
    database_controller,
    manager_controller,
    main_menu_controller,
    obj_creation_controller,
    object_type,
    selection_enabled=False,
    question="",
    additional_item_create=False,
    additional_item_end=False,
    reduce=False,
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
        print("Liste des joueurs :")
        initial_list = Player.deserialize_players(
            database_controller.read_db("players")
        )
    elif object_type == Tournament:
        print("Liste des tournois :")
        initial_list = Tournament.deserialize_tournament(
            database_controller.read_db("tournaments")
        )
    else:
        print("Entrez un Tournois ou un joueur.")
        return
    id = 1
    if reduce:
        for object in initial_list:
            if len(object.leaderboard) != 0:
                final_list.append(object)
                manager_controller.view_object(object, id)
                id += 1
    else:
        for object in initial_list:
            final_list.append(object)
            manager_controller.view_object(object, id)
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
        selected_id = input(question + " (Entrer 'R' pour revenir au menu principal)")
        if selected_id.upper() == "R":
            clear_console()
            main_menu = main_menu_controller()
            main_menu.select(input("Entrez votre réponse : "))
        try:
            selected_id = int(selected_id)
        except ValueError:
            print("Entrez un numéro valide ou 'R'")
            return
        if selected_id < 1 or selected_id > len(final_list) + 2:
            print("Entrez un numéro valide ")
            return
        if selected_id == len(final_list) + 1:
            if object_type == Player:
                player_creator = obj_creation_controller()
                player_creator.create_new()
            elif object_type == Tournament:
                tournament_creator = obj_creation_controller()
                tournament_creator.create_new()
        if selected_id == len(final_list) + 2:
            return "End"
        selected_object: Union[Player, Tournament] = final_list[selected_id - 1]
        return selected_object
    else:
        input("Appuyez sur entrée pour revenir au menu principal")
        clear_console()
        main_menu = main_menu_controller()
        main_menu.select(input("Entrez votre réponse : "))
