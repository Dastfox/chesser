from typing import Union
from views.object_view import Object_view
from controllers.manager_controller import Manager
from models.players import Player
from models.tournament import Tournament
from utils import clear_console
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
        object_type: The type of object whose list is to be viewed.
         Can be either a Player object or a Tournament object.
        selection_enabled: A boolean value that indicates whether
         to allow user to select an object from the list.
        question: A string that will be printed if selection_enabled is True,
         asking the user which object to select.

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
        for object in initial_list:
            boolean = callback_condition_for_display(object)
            if boolean:
                liste.append(object)
        initial_list = liste

    id = 1

    if len(initial_list) == 0:
        if callback_condition_for_display:
            print("Aucun tournois pouvant être affiché")
            print("dans ce menu n'a été trouvé.")
            if not additional_item_create:
                input("Retour au menu...")
                return "back"
        if not additional_item_create:
            input("Aucun objet trouvé. Retour au menu...")
            return "back"

    for object in initial_list:
        final_list.append(object)
        Manager.view_object(object, id)
        id += 1
    if additional_item_create:
        Object_view.view_additional_options(id, additional_item_end)
    if selection_enabled:
        selected_id = ""
        selected_id = input(
            question + " (Entrer 'R' pour revenir au menu principal)"
        )
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
            return "end"
        selected_object: Union[Player, Tournament] = final_list[
            selected_id - 1
        ]
        return selected_object
    else:
        input("Appuyez sur entrée pour revenir au menu principal")
        clear_console()
