import time
from controllers.db_controller import Database
from views.lists_view import List_view
from controllers.manager_controller import Manager
from controllers.player_controller import PlayerCreation, PlayerList
from controllers.tournament_controller import PlayTournamentController
from controllers.tournament_controller import TournamentCreation, TournamentList
from controllers.tournament_controller import (
    Leaderboard,
)
from views.menu_view import *
from utils import clear_console


class MainMenu:
    def __init__(self) -> None:
        """
        Initializes the main menu
        """
        clear_console()
        print_main = Menus_views.main_menu()

    def select(self, selector: int):
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
                option_play_tournament = play_tournament_menu.select(
                    input("Selection : ")
                )
            elif selector == "2":
                player_menu = PlayerMenu()
                option_player = player_menu.select(input("Selection : "))
            elif selector == "3":
                tournament_management = TournamentMenu()
                option_tournament = tournament_management.select(input("Selection : "))
            elif selector == "4":
                leaderboard = Leaderboard()
                main_menu = MainMenu()
                main_menu_selector = main_menu.select(input("Entrez votre réponse : "))
            elif selector == "5":
                exit()

            else:
                print("Cette option n'existe pas, veuillez réessayer")
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )


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
        print_tournament_menu = Menus_views.tournament_menu()

    def select(self, selector: int):
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
                option_play_tournament = play_tournament.select(input("Selection : "))

            elif selector == "2":
                tournament_creation = TournamentCreation()
                create_tournament = tournament_creation.create_new()
                main_menu = MainMenu()
                main_menu.select(input("Entrez votre réponse : "))

            elif selector == "3":
                tournament_list = TournamentList()
                tournament = tournament_list.view_list()
                while tournament is None:
                    tournament = tournament_list.view_list()
                if tournament is "back":
                    return_back = TournamentMenu()
                    main_menu_selector = return_back.select(
                        input("Entrez votre réponse : ")
                    )
                else:
                    tournament_submenu = TournamentSubMenu(tournament)
                    tournament_submenu.select(
                        input("Entrez votre réponse : "), tournament
                    )

            elif selector == "4":
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = TournamentMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )


class TournamentSubMenu:
    def __init__(self, tournament: Tournament):
        clear_console()
        """
        Initialize the tournament menu.
        """
        Manager.view_object(tournament)
        Menus_views.tournament_submenu()

    def select(self, selector: int, tournament: Tournament):
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
                see_players = TournamentList()
                clear_console()
                Manager.view_object(tournament)
                print("Liste des joueurs du tournois sélectionné :")
                if len(tournament.players) == 0:
                    print("Aucun joueur n'a été ajouté à ce tournoi")
                else:
                    player_dict = Player.deserialize_players(tournament.players)
                    for player in player_dict:
                        Manager.view_object(player)
                input("Appuyez sur entrée pour revenir au menu précédent")
                return_back = TournamentSubMenu(tournament)
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : "), tournament
                )

            elif selector == "2":
                see_matches = TournamentList()
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
                        for idx, match in enumerate(round.matches):
                            match_deserialized = (
                                Player.deserialize_players([match[0]])[0],
                                Player.deserialize_players([match[1]])[0],
                                match[2],
                            )
                            List_view.view_match(match_deserialized, 0, True)

                input("Appuyez sur entrée pour revenir au menu précédent")
                return_back = TournamentSubMenu(tournament)
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : "), tournament
                )
            elif selector == "3":
                Database.delete_db_object(tournament.name, "tournaments")
                clear_console()
                print("Le tournoi a bien été supprimé")
                time.sleep(1)
                return_back = TournamentMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            elif selector == "4":
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = TournamentSubMenu(tournament)
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : "), tournament
                )


class PlayTournamentMenu:
    def __init__(self):
        clear_console()
        """
        Initialize the tournament play.
        """
        Menus_views.play_tournament_menu()

    def select(self, selector: int):
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
                back = return_back.select(input("Entrez votre réponse : "))
            elif selector == "2":
                play_tournament_controller = PlayTournamentController()
                play_tournament_controller.play_a_round()
                return_back = PlayTournamentMenu()
                back = return_back.select(input("Entrez votre réponse : "))
            elif selector == "3":
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = PlayTournamentMenu()
                return_back = return_back.select(input("Entrez votre réponse : "))


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
        print_playermenu = Menus_views.players_menu()

    def select(self, selector: int, main_menu_controller=None):
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
                new_player = add_player.create_new()
            elif selector == "2":
                player_list = PlayerList()
                player_list.view_list()
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            elif selector == "3":
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = PlayerMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
