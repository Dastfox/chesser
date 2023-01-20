from controllers.db_controller import Database
from controllers.manager_controller import Manager
from controllers.list_controller import view_list
from views.menu_view import *
from utils import clear_console
from utils import yes_or_no


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
        else:
            player_dict = Manager.object_list_fitting_db(self.players_list)
            Database.export_to_db(player_dict, "players")


class PlayerList:
    """A class representing the player list in a game.

    Attributes:
        None
    """

    def __init__(self):
        clear_console()

    def view_list(self):
        """View the list of tournaments.

        Returns:
            None
        """
        clear_console()
        list = view_list(
            PlayerCreation,
            Player,
        )
