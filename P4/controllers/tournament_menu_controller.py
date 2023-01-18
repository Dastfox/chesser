import time
from models.round import Round
from views.lists_view import List_view
from controllers.db_controller import Database
from controllers.manager_controller import Manager
from models.tournament import Tournament, serialize_tournament
from views.menu_view import *
from utils import clear_console
import colorama
from controllers.list_controller import view_list

"""
leaderboard
"""


class Leaderboard:
    def __init__(
        self,
        main_menu_controller,
        tournament: Tournament = None,
    ) -> None:
        clear_console()
        if tournament is None:
            selected_tournament = view_list(
                Database, Manager, main_menu_controller, Tournament, True
            )
        else:
            selected_tournament = tournament
        players = Player.deserialize_players(selected_tournament.players)
        players.sort(key=lambda x: x.points, reverse=True)
        clear_console()
        for i, player in enumerate(players):
            if i == 0:
                print(
                    colorama.Back.YELLOW
                    + colorama.Fore.RED
                    + colorama.Style.BRIGHT
                    + "\n---- 1 ----"
                    + colorama.Style.RESET_ALL
                )
                player.rank = 1
            elif i == 1:
                print(
                    colorama.Back.CYAN
                    + colorama.Fore.YELLOW
                    + colorama.Style.BRIGHT
                    + "\n---- 2 ----"
                    + colorama.Style.RESET_ALL
                )
                player.rank = 2
            elif i == 2:
                print(
                    colorama.Back.MAGENTA
                    + colorama.Fore.WHITE
                    + colorama.Style.BRIGHT
                    + "\n---- 3 ----"
                    + colorama.Style.RESET_ALL
                )
                player.rank = 3
            else:
                player.rank = i + 1
            List_view.view_player(player)
        input("Appuyez sur Entrée pour continuer...")
        main_menu = main_menu_controller()
        main_menu.select(input("Entrez votre réponse : "))


"""
Tounaments
"""


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

    def select(self, selector: int, main_menu_controller):
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
                start_tournament = 1
            elif selector == "2":
                tournament_creation = TournamentCreation()
                create_tournament = tournament_creation.create_new()
            elif selector == "3":
                tournament_list = TournamentList()
                tournament_list.view_list(main_menu_controller)
            elif selector == "4":
                return_back = main_menu_controller()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = TournamentMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )


class TournamentList:
    """A class representing the tournament list in a game.

    Attributes:
        None
    """

    def __init__(self):
        self.tournaments = []

    def view_list(self, main_menu_controller):
        """View the list of tournaments.

        Returns:
            None
        """
        clear_console()
        selected_tournament: Tournament = view_list(
            Database,
            Manager,
            main_menu_controller,
            TournamentCreation,
            Tournament,
            selection_enabled=True,
            question="Sélectionnez un tournoi pour afficher ses joueurs",
        )
        clear_console()
        Manager.view_object(selected_tournament)
        print("Liste des joueurs du tournois sélectionné :")
        if len(selected_tournament.players) == 0:
            print("Aucun joueur n'a été ajouté à ce tournoi")

        else:
            player_dict = Player.deserialize_players(selected_tournament.players)
            for player in player_dict:
                Manager.view_object(player)

        input("Appuyez sur entrée pour revenir au menu principal")
        main_menu = main_menu_controller()
        main_menu.select(input("Entrez votre réponse : "))


class TournamentCreation:
    def __init__(self, tournament_list=[]) -> None:

        self.tournament_list: list[Tournament] = tournament_list
        TournamentCreationView.tournament_creation()

    @staticmethod
    def date_validator(date: str) -> bool:
        if len(date) != 8:
            return False
        if not date.isnumeric():
            return False
        day = int(date[0:2])
        month = int(date[2:4])
        year = int(date[4:8])
        if day < 1 or day > 31:
            return False
        if month < 1 or month > 12:
            return False
        if year < 1900 or year > 2078:
            return False
        return True

    def create_new(self):
        """
        Create a new tournament object and add it to the database.

        The user will be prompted to enter the name, location, start and end dates, time control,
        round amount, and description of the tournament. These values will be used to create a new
        Tournament object, which will then be added to the database.
        """
        # init variables
        name = ""
        location = ""
        date_start = ""
        date_end = ""
        date = ""
        time_control = ""
        description = ""
        round_amount = 4
        players = []
        turn = {}

        # Prompt the user to enter the name of the tournament
        while not name:
            if name != " ":
                print("Veuillez entrer un nom")
            name = input("Nom : ")

        # Prompt the user to enter the location of the tournament
        while not location:
            if location != " ":
                print("Veuillez entrer un lieu")
            location = input("Localisation : ")

        # Prompt the user to enter the start and end dates of the tournament
        while not TournamentCreation.date_validator(
            date_start
        ) or not TournamentCreation.date_validator(date_end):
            if date_start != "" and date_end != "" and date_start > date_end:
                print(
                    "Veuillez entrer une date de début et de fin valide",
                    date_start,
                    ">",
                    date_end,
                )
            while not TournamentCreation.date_validator(date_start):
                if date_start != "":
                    print("Veuillez entrer une date de début valide")
                date_start = input("Date de début : ")
            while not TournamentCreation.date_validator(date_end):
                if date_end != "":
                    print("Veuillez entrer une date de fin valide")
                date_end = input("Date de fin : ")

        # Prompt the user to enter the time control for the tournament
        time_control = input("Controle de temps \n(blitz, bullet ou coup rapide): ")

        # Prompt the user to enter the round amount for the tournament (default is 4)
        round_amount = input("Nombre de tours (4 par défaut) : ")

        if round_amount == "":
            round_amount = 4

        # Prompt the user to enter a description for the tournament
        description = input("Description : ")

        # Format the date range as a string
        date = f"{date_start} - {date_end}"

        # Create a new Tournament object with the user-provided values
        new_tournament = Tournament(
            name, location, date, round_amount, turn, players, time_control, description
        )

        # Add the new tournament to the database
        list = []
        list.append(new_tournament)
        tournament_dict = Manager.object_list_fitting_db(list)
        Database.export_to_db(tournament_dict, "tournaments")

        # Confirm that the tournament has been added to the database
        clear_console()
        print(new_tournament.name, "a été ajouté à la base de données")
        time.sleep(1)
        main_menu = MainMenu()
        main_menu.select(input("Entrez votre réponse : "))


"""
Play Tournament Menu.
"""


class PlayTournamentMenu:
    def __init__(self):
        clear_console()
        """
        Initialize the tournament play.
        """
        Menus_views.play_tournament_menu()

    def select(self, selector: int, main_menu_controller):
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
                self.add_players_to_tournament(main_menu_controller)
            elif selector == "2":
                self.play_a_round()
            elif selector == "3":
                return_back = main_menu_controller
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = TournamentMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : "), main_menu_controller
                )

    def add_players_to_tournament(self, main_menu_controller):
        clear_console()
        print("Welcome to the tournament.")
        tournament = self.select_tournament(main_menu_controller)
        if tournament is None:
            create_new = input(
                "No tournament found, would you like to create one? (y/n)"
            )
            if create_new.lower() == "y":
                tournament = self.create_tournament()
            else:
                return
        players = self.select_players(main_menu_controller)
        for player in players:
            player.points = 0
        tournament.players = players
        tournament_db = serialize_tournament(tournament)
        Database.update_by_name(tournament.name, tournament_db, "tournaments")

        clear_console()
        print(len(players), "joueur ajoutés au tournois")
        time.sleep(2)
        return_back = PlayTournamentMenu()
        return_back.select(input("Entrez votre réponse : "))

    def select_tournament(self, main_menu_controller):
        selected_tournament = view_list(
            Database,
            Manager,
            main_menu_controller,
            TournamentCreation,
            Tournament,
            True,
            "\n\nSélectionnez un tournois: ",
            True,
        )
        return selected_tournament

    def create_tournament(self):
        tournament_creation = TournamentCreation()
        tournament_creation.create_new()

    def select_players(self, main_menu_controller):
        # players = Database.read_db("players")
        selected_players = []
        while True:
            new_player = view_list(
                Database,
                Manager,
                main_menu_controller,
                TournamentCreation,
                Player,
                True,
                "Select a player by number or create a new player: ",
                True,
                True,
            )
            if new_player != "End":
                selected_players.append(Player.player_format_fitting_db(new_player))
                print(selected_players)
            else:
                return selected_players

    def play_a_round(self, main_menu_controller, tournament: Tournament = None):
        if tournament is None:
            selected_tournament: Tournament = view_list(
                Database,
                Manager,
                main_menu_controller,
                TournamentCreation,
                Tournament,
                True,
                "\n\nSélectionnez un tournois: ",
                True,
            )
        else:
            selected_tournament = tournament

        if selected_tournament.rounds and len(selected_tournament.rounds) > 0:
            last_round: Round = selected_tournament.rounds[-1]
            if last_round.is_finished == True:
                last_round = selected_tournament.generate_pairs()
        else:
            last_round = selected_tournament.generate_pairs()

        round = last_round

        clear_console()

        for match in round.matches:
            print("match", match)
            match_player = [
                Player.deserialize_players([match[0]])[0],
                Player.deserialize_players([match[1]])[0],
                match[2],
            ]
            List_view.view_match(match_player)

        if yes_or_no("Jouer la ronde?"):
            clear_console()
            selected_tournament.play_round()

        Database.update_by_name(
            selected_tournament.name,
            serialize_tournament(selected_tournament),
            "tournaments",
        )
        if selected_tournament.rounds[-1].is_finished == True:
            if selected_tournament.round_amount > len(selected_tournament.rounds):
                leaderboard = Leaderboard(
                    main_menu_controller,
                    selected_tournament,
                )
                input("Appuyez sur entrée pour continuer")
            elif yes_or_no("Générer les matchups pour une autre ronde?"):
                clear_console()
                self.play_a_round(selected_tournament)

        main_menu = PlayTournamentMenu()
        main_menu.select(input("Entrez votre réponse : "))


"""
Utilities.
"""


def yes_or_no(question):
    """Ask a yes or no question.

    Args:
        question (str): The yes or no question to be asked.

    Returns:
        bool: True if the answer is "yes", False if the answer is "no".

    Raises:
        ValueError: If the answer is not "yes" or "no".
    """
    answer = input(question + "(O/n): ").lower().strip()
    print("")
    while not (answer == "o" or answer == "oui" or answer == "n" or answer == "non"):
        print("Entrez oui ou non")
        answer = input(question + "(O/n):").lower().strip()
        print("")
    if answer[0] == "o":
        return True
    else:
        return False
