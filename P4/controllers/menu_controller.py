import json
from multiprocessing import managers
from operator import ge
from controllers.db_controller import Database
from controllers.manager_controller import Manager
from models.players import Player
from models.tournament import Tournament
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
                play_tournament = 1
            elif selector == "2":
                player_menu = PlayerMenu()
                option_player = player_menu.select(input("Selection : "))
            elif selector == "3":
                tournament_management = TournamentMenu()
                option_tournament = tournament_management.select(input("Selection : "))
            elif selector == "4":
                exit()
            else:
                print("Cette option n'existe pas, veuillez réessayer")
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )


class PlayerMenu:
    """A class representing the player menu in a game.

    Attributes:
        None
    """

    def __init__(self) -> None:
        clear_console()
        """Initialize the player menu.

        Prints the options for the player menu.
        """
        print_playermenu = Menus_views.players_menu()

    def select(self, selector: int):
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
                view_list(Player)
            elif selector == "3":
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = MainMenu()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )


class PlayerCreation:
    """A class for creating new player objects.

    Attributes:
        players_list (list[Player]): A list of player objects.
    """

    def __init__(self, players_list=[]) -> None:
        clear_console()
        """Initialize the player creation process.

        Prints the player creation menu.

        Args:
            players_list (list[Player], optional): A list of player objects. Defaults to an empty list.
        """
        self.players_list: list[Player] = players_list
        PlayerCreationView.player_creation()

    def create_new(self):
        """Create a new player object.

        Prompts the user for input for the player's first name, last name, birthdate, gender, and rank. Validates the input and creates a new player object with the provided information. Appends the new player object to the players list.

        Returns:
            None
        """
        first_name = ""
        last_name = ""
        birthdate = ""
        day = 0
        month = 0
        year = 0
        gender = ""
        rank = ""

        # validator first_name
        while not first_name.isalpha():
            if first_name != "":
                print("\nVeuillez entrer un prénom valide")
            first_name = input("\nPrénom : ")

        # validator last_name
        while not last_name.isalpha():
            if last_name != "":
                print("\nVeuillez entrer un nom valide")
            last_name = input("\nNom : ")

        # validator birthdate

        while not (
            day > 0
            and day < 32
            and month > 0
            and month < 13
            and year > 1900
            and year < 2022
        ):
            # while not (birthdate.isnumeric() and len(birthdate) == 8) :
            if birthdate != "":
                print("\nVeuillez entrer une date de naissance valide")
            birthdate = input("\nDate de naissance (jjmmaaaa) : ")
            if len(birthdate) == 8 and birthdate.isnumeric():
                day = int(birthdate[0:2])
                month = int(birthdate[2:4])
                year = int(birthdate[4:8])

        gender = input("\nGenre (H/F/Na) : ")
        while not gender == "H" and gender == "F" and gender == "Na":
            print("\nVeuillez entrer un genre valide")
            gender = input("\nGenre (H/F/Na) : ")

        rank = input("\nClassement : ")
        while not rank.isnumeric():
            print("\nVeuillez entrer un classement valide")
            rank = input("\nClassement : ")

        new_player = Player(first_name, last_name, birthdate, gender, rank)
        self.players_list.append(new_player)
        player_list_lenth = len(
            Player.player_format_fitting_python(Database.read_db("players"))
        )

        if (len(self.players_list) + player_list_lenth) < 8:
            print("\n" + first_name, last_name, " a bien été ajouté")
            answer = PlayerCreation.yes_or_no(
                PlayerCreationView.ask_again().format(
                    len(self.players_list) + player_list_lenth
                )
            )
            # answer yes
            if answer == True:
                self.create_new()
            # answer no
            else:
                print(
                    "\nVous avez ajouté",
                    len(self.players_list) + player_list_lenth,
                    "joueurs",
                )
                player_dict = Manager.object_list_fitting_db(self.players_list)
                saving_list = Database.export_to_db(player_dict, "players")
                return_back = PlayerMenu()
                return_back.select(input("\nEntrez votre réponse : "))
        else:
            player_dict = Manager.object_list_fitting_db(self.players_list)
            Database.export_to_db(player_dict, "players")
            main_menu = MainMenu()
            main_menu.select(input("Entrez votre réponse : "))

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
        while not (
            answer == "o" or answer == "oui" or answer == "n" or answer == "non"
        ):
            print("Entrez oui ou non")
            answer = input(question + "(O/n):").lower().strip()
            print("")
        if answer[0] == "o":
            return True
        else:
            return False


def view_list(object_type):
    clear_console()
    """View a list of objects.

    Args:
        object_type: The type of object whose list is to be viewed. Can be either a Player object or a Tournament object.

    Returns:
        None
    """
    final_list = []
    initial_list = []
    if object_type == Player:
        print("Liste des joueurs :")
        initial_list = Player.player_format_fitting_python(Database.read_db("players"))
    elif object_type == Tournament:
        print("Liste des tournois :")
        initial_list = Tournament.tournament_format_fitting_python(
            Database.read_db("tournaments")
        )
    else:
        print("Invalid object type. Please pass either Player or Tournament.")
        return
    id = 1
    for object in initial_list:
        print(object)
        final_list.append(object)
        Manager.view_object(object, id)
        id += 1

    input("Appuyez sur entrée pour revenir au menu principal")
    clear_console()
    main_menu = MainMenu()
    main_menu.select(input("Entrez votre réponse : "))


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
                start_tournament = 1
            elif selector == "2":
                tournament_creation = TournamentCreation()
                create_tournament = tournament_creation.create_new()
            elif selector == "3":
                view_list(Tournament)
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
        if year < 1900 or year > 2022:
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
        print(new_tournament.name, "a été ajouté à la base de données")
        main_menu = MainMenu()
        main_menu.select(input("Entrez votre réponse : "))

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
            print(f"Le joueur {player.first_name} {player.last_name} a été ajouté au tournoi {tournament.name}.")
        else:
            print(f"Le joueur {player.first_name} {player.last_name} est déjà présent dans le tournoi {tournament.name}.")