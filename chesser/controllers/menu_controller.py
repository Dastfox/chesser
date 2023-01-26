import time
from controllers.db_controller import Database
from views.lists_view import List_view
from controllers.manager_controller import Manager
from controllers.player_controller import PlayerCreation, PlayerList
from controllers.tournament_controller import PlayTournamentController
from controllers.tournament_controller import (
    TournamentCreation,
    TournamentList,
)
from models.players import Player
from models.tournament import Tournament
from controllers.tournament_controller import (
    Leaderboard,
)
from views.menu_view import Menus_views
from utils import clear_console


class MainMenu:
    def __init__(self) -> None:
        """
        Initializes the main menu
        """
        clear_console()
        Menus_views.main_menu()

    def select(self, selector: str):
        """
        Selects the option chosen by the user in the main menu

        Parameters:
        selector (int): the selected option by the user

        Returns:
        None
        """
        while True:
            if selector == "1":
                play_tournament_menu = PlayTournamentMenu()
                play_tournament_menu.select(input("Selection : "))
            elif selector == "2":
                player_menu = PlayerMenu()
                player_menu.select(input("Selection : "))
            elif selector == "3":
                tournament_management = TournamentMenu()
                tournament_management.select(input("Selection : "))
            elif selector == "4":
                Leaderboard()
                main_menu = MainMenu()
                main_menu.select(input("Entrez votre réponse : "))
            elif selector == "5":
                exit()

            else:
                print("Cette option n'existe pas, veuillez réessayer")
                return_back = MainMenu()
                return_back.select(input("Entrez votre réponse : "))


class TournamentMenu:
    """A class representing the tournament menu in a game.

    Attributes:
        None
    """

    def __init__(self) -> None:
        clear_console()
        """Initialize the tournament menu.

        Prints the options for the tournament menu.
        """
        Menus_views.tournament_menu()

    def select(self, selector: str):
        """Select an option from the tournament menu.

        Args:
            selector: An integer representing the selected option.

        Returns:
            None

        Raises:
            TypeError: If the selector is not a valid integer.
        """
        while True:
            if selector == "1":
                play_tournament = PlayTournamentMenu()
                play_tournament.select(input("Selection : "))

            elif selector == "2":
                tournament_creation = TournamentCreation()
                tournament_creation.create_new()
                main_menu = MainMenu()
                main_menu.select(input("Entrez votre réponse : "))

            elif selector == "3":
                tournament_list = TournamentList()
                tournament = tournament_list.view_list()
                while tournament is None:
                    tournament = tournament_list.view_list()
                if tournament == "back" or tournament == "end":
                    return_back = TournamentMenu()
                    return_back.select(input("Entrez votre réponse : "))
                elif isinstance(tournament, Tournament):
                    tournament_submenu = TournamentSubMenu(tournament)
                    tournament_submenu.select(
                        input("Entrez votre réponse : "), tournament
                    )
                else:
                    print(
                        "Cette option n'est pas disponible, veuillez réessayer"
                    )
                    return_back = TournamentMenu()
                    return_back.select(input("Entrez votre réponse : "))

            elif selector == "4":
                return_back = MainMenu()
                return_back.select(input("Entrez votre réponse : "))
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = TournamentMenu()
                return_back.select(input("Entrez votre réponse : "))


class TournamentSubMenu:
    def __init__(self, tournament: Tournament):
        clear_console()
        """
        Initialize the tournament menu.
        """
        Manager.view_object(tournament)
        Menus_views.tournament_submenu()

    def select(self, selector: str, tournament: Tournament):
        """Select an option from the tournament menu.

        Args:
            selector: An integer representing the selected option.

        Returns:
            None

        Raises:
            TypeError: If the selector is not a valid integer.
        """
        while True:
            if selector == "1":
                TournamentList()
                clear_console()
                Manager.view_object(tournament)
                print("Liste des joueurs du tournois sélectionné :")
                if len(tournament.players) == 0:
                    print("Aucun joueur n'a été ajouté à ce tournoi")
                else:
                    if all(isinstance(i, Player) for i in tournament.players):
                        player_as_obj = tournament.players
                    else:
                        return

                    for player in player_as_obj:
                        Manager.view_object(player)
                input("Appuyez sur entrée pour revenir au menu précédent")
                return_back = TournamentSubMenu(tournament)
                return_back.select(
                    input("Entrez votre réponse : "), tournament
                )

            elif selector == "2":
                TournamentList()
                clear_console()
                Manager.view_object(tournament)
                print("Liste des matchs du tournois sélectionné :")
                no_matches = True
                for round in tournament.rounds:
                    for match in round.matches:
                        if match:
                            no_matches = False
                if no_matches:
                    print("Aucun match n'a été ajouté à ce tournoi")
                else:
                    for round in tournament.rounds:
                        print("---------", round.id, "---------")
                        if round.is_finished:
                            print("Statut de la ronde : Terminée")
                        else:
                            print("Statut de la ronde : En cours")

                        print("Liste des matchs de la ronde :\n")
                        for match in round.matches:
                            match_deserialized = (
                                Player.deserialize_players([match[0]])[0],
                                Player.deserialize_players([match[1]])[0],
                                match[2],
                            )
                            List_view.view_match(match_deserialized, 0, True)

                input("Appuyez sur entrée pour revenir au menu précédent")
                return_back = TournamentSubMenu(tournament)
                return_back.select(
                    input("Entrez votre réponse : "), tournament
                )
            elif selector == "3":
                Database.delete_db_object(tournament.name, "tournaments")
                clear_console()
                print("Le tournoi a bien été supprimé")
                time.sleep(1)
                return_back = TournamentMenu()
                return_back.select(input("Entrez votre réponse : "))
            elif selector == "4":
                return_back = MainMenu()
                return_back.select(input("Entrez votre réponse : "))
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = TournamentSubMenu(tournament)
                return_back.select(
                    input("Entrez votre réponse : "), tournament
                )


class PlayTournamentMenu:
    def __init__(self):
        clear_console()
        """
        Initialize the tournament play.
        """
        Menus_views.play_tournament_menu()

    def select(self, selector: str):
        """Select an option from the tournament menu.

        Args:
            selector: An integer representing the selected option.

        Returns:
            None

        Raises:
            TypeError: If the selector is not a valid integer.
        """
        while True:
            if selector == "1":
                play_tournament = PlayTournamentController()
                play_tournament.add_players_to_tournament()
                return_back = PlayTournamentMenu()
                return_back.select(input("Entrez votre réponse : "))
            elif selector == "2":
                play_tournament_controller = PlayTournamentController()
                play_tournament_controller.play_a_round()
                return_back = PlayTournamentMenu()
                return_back.select(input("Entrez votre réponse : "))
            elif selector == "3":
                return_back = MainMenu()
                return_back.select(input("Entrez votre réponse : "))
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = PlayTournamentMenu()
                return_back = return_back.select(
                    input("Entrez votre réponse : ")
                )


"""
Players
"""


class PlayerMenu:
    """A class representing the player menu in a game.

    Attributes:
        None
    """

    def __init__(self) -> None:
        """Initialize the player menu.

        Prints the options for the player menu.
        """
        clear_console()
        Menus_views.players_menu()

    def select(self, selector: str, main_menu_controller=None):
        """Select an option from the player menu.

        Args:
            selector: An integer representing the selected option.

        Returns:
            None

        Raises:
            TypeError: If the selector is not a valid integer.
        """
        while True:
            if selector == "1":
                add_player = PlayerCreation()
                add_player.create_new()
                return_back = PlayerMenu()
                return_back.select(input("Entrez votre réponse : "))
            elif selector == "2":
                player_list = PlayerList()
                player_list.view_list()
                return_back = MainMenu()
                return_back.select(input("Entrez votre réponse : "))
            elif selector == "3":
                return_back = MainMenu()
                return_back.select(input("Entrez votre réponse : "))
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = PlayerMenu()
                return_back.select(input("Entrez votre réponse : "))
