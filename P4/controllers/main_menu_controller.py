from controllers.player_menu_controller import PlayerMenu
from controllers.tournament_menu_controller import (
    Leaderboard,
    PlayTournamentMenu,
    TournamentMenu,
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
                    input("Selection : "), MainMenu
                )
            elif selector == "2":
                player_menu = PlayerMenu()
                option_player = player_menu.select(input("Selection : "), MainMenu)
            elif selector == "3":
                tournament_management = TournamentMenu()
                option_tournament = tournament_management.select(
                    input("Selection : "), MainMenu
                )
            elif selector == "4":
                leaderboard = Leaderboard()
            elif selector == "5":
                exit()

            else:
                print("Cette option n'existe pas, veuillez réessayer")
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
