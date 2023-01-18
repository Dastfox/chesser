from controllers.db_controller import Database
from controllers.manager_controller import Manager
from views.menu_view import *
from utils import clear_console
from controllers.list_controller import view_list

"""
Players
"""


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
                new_player = add_player.create_new(
                    main_menu_controller=main_menu_controller
                )
            elif selector == "2":
                view_list(
                    Database,
                    Manager,
                    main_menu_controller,
                    PlayerCreation,
                    Player,
                )
            elif selector == "3":
                return_back = main_menu_controller()
                main_menu_selector = return_back.select(
                    input("Entrez votre réponse : ")
                )
            else:
                print("Cette option n'est pas disponible, veuillez réessayer")
                return_back = main_menu_controller()
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

    def create_new(self, main_menu_controller=None):
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
        player_list_lenth = len(Player.deserialize_players(Database.read_db("players")))

        if (len(self.players_list) + player_list_lenth) < 8:
            print("\n" + first_name, last_name, " a bien été ajouté")
            answer = yes_or_no(
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
            main_menu = main_menu_controller()
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
    while not (answer == "o" or answer == "oui" or answer == "n" or answer == "non"):
        print("Entrez oui ou non")
        answer = input(question + "(O/n):").lower().strip()
        print("")
    if answer[0] == "o":
        return True
    else:
        return False
