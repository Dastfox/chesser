from colorama import Fore, Style, Back
from models.players import Player


class Object_view:
    @staticmethod
    def view_player(player: Player, id: int = 0):
        """
        Prints a formatted representation of a Player object.
        Optional parameters include an id and whether to print
         the player's rank.

        Example:
        >>> player = Player("John", "Doe", "123456", "01012000", "M", 25)
        >>> view_player(player, id=1, print_rank=True)
        -----  1  -----
        Prénom : John
        Nom : Doe
        ID FFE : 123456
        Date de naissance : 01 / 01 / 2000
        Genre : M
        Rang : 25
        """
        id_as_str = str(id)
        if id != 0:
            print(
                Fore.YELLOW
                + "-----  "
                + id_as_str
                + "  -----"
                + Style.RESET_ALL
            )
        print(Fore.YELLOW + "\nPrénom :", player.first_name + Style.RESET_ALL)
        print(Fore.YELLOW + "Nom :", player.last_name + Style.RESET_ALL)
        print(Fore.YELLOW + "ID FFE :", player.chess_id + Style.RESET_ALL)
        print(
            Fore.YELLOW + "Date de naissance :",
            player.birthdate[0:2],
            "/",
            player.birthdate[2:4],
            "/",
            player.birthdate[4:8],
            Style.RESET_ALL,
        )
        if player.gender:
            print(Fore.YELLOW + "Genre :", player.gender + Style.RESET_ALL)

    @staticmethod
    def view_tournament(tournament, id: int = 0):
        """
        Prints the details of a tournament in a formatted way.

        :param tournament: An instance of the Tournament class.
        :param id: (optional) An id number for the tournament.
        :return: None

        Example:
        >>> tournament = Tournament(
            "My Tournament",
            "New York City",
            "2022-01-01",
            ["Player 1", "Player 2"],
            3,
            "blitz",
            "This is a tournament."
        >>> view_tournament(tournament, 1)
        -----  1  -----
        Nom : My Tournament
        Localisation : New York City🌍
        Date : 2022-01-01📅
        Nombre de joueurs : 2👤
        Nombre de tours : 3🎲
        Contrôle de temps : blitz
        Description :📝
        """
        round_as_str = str(tournament.round_amount)
        id_as_str = str(id)
        player_amount_as_str = str(len(tournament.players))
        if id != 0:
            print(
                Fore.YELLOW
                + "-----  "
                + id_as_str
                + "  -----"
                + Style.RESET_ALL
            )
        print(Fore.YELLOW + "\nNom :", tournament.name + Style.RESET_ALL)
        print(
            Fore.YELLOW + "Localisation :",
            tournament.location + "🌍" + Style.RESET_ALL,
        )
        print(Fore.YELLOW + "Date :", tournament.date + "📅" + Style.RESET_ALL)
        print(
            Fore.YELLOW + "Nombre de joueurs :",
            player_amount_as_str + "👤" + Style.RESET_ALL,
        )
        print(
            Fore.YELLOW + "Nombre de tours :",
            round_as_str + "🎲" + Style.RESET_ALL,
        )
        print(
            Fore.YELLOW + "Contrôle de temps :",
            tournament.time_control + "⏰" + Style.RESET_ALL,
        )
        print(
            Fore.YELLOW
            + "Description :"
            + tournament.description
            + "📝"
            + Style.RESET_ALL
        )

    @staticmethod
    def view_match(match, id: int = 0, print_reslut: bool = False):
        """
        Affiche les informations d'un match.

        Exemple:
        ------ 3 -------
        Joueur blanc : John Doe contre Joueur noir : Jane Doe
        Gagnant : John Doe

        """

        id_as_str = str(id)
        p1: Player = match[0]
        p2: Player = match[1]
        result = match[2]
        if id != 0:
            print(
                Fore.YELLOW
                + "-----  "
                + id_as_str
                + "  -----"
                + Style.RESET_ALL
            )
        print(
            Fore.WHITE + "Joueur blanc :",
            p1.first_name
            + " "
            + p1.last_name
            + Style.RESET_ALL
            + Fore.YELLOW
            + " contre "
            + Style.RESET_ALL
            + Fore.BLUE
            + "Joueur noir : "
            + p2.first_name
            + " "
            + p2.last_name
            + Style.RESET_ALL,
        )
        if print_reslut and result in ("1", "2", "D", "d"):
            if result == "1":
                print(
                    Fore.YELLOW + "Gagnant :",
                    p1.first_name + " " + p1.last_name + Style.RESET_ALL,
                )
            elif result == "2":
                print(
                    Fore.YELLOW + "Gagnant :",
                    p2.first_name + " " + p2.last_name + Style.RESET_ALL,
                )
            else:
                print(Fore.YELLOW + "Match nul" + Style.RESET_ALL)
        print("\n")

    @staticmethod
    def view_leaderboard(players: list[Player]):
        """
        ----- Leaderboard -----
        player view with rank & podium
        """
        players.sort(key=lambda x: x.rank, reverse=True)
        print(Fore.YELLOW + "-----  Leaderboard  -----" + Style.RESET_ALL)
        for i, player in enumerate(players):
            if i == 0:
                print(
                    Back.YELLOW
                    + Fore.RED
                    + Style.BRIGHT
                    + "\n---- 1 ----"
                    + Style.RESET_ALL
                )
            elif i == 1:
                print(
                    Back.CYAN
                    + Fore.YELLOW
                    + Style.BRIGHT
                    + "\n---- 2 ----"
                    + Style.RESET_ALL
                )
            elif i == 2:
                print(
                    Back.MAGENTA
                    + Fore.WHITE
                    + Style.BRIGHT
                    + "\n---- 3 ----"
                    + Style.RESET_ALL
                )
            else:
                print(
                    Fore.WHITE
                    + "\n---- "
                    + str(i + 1)
                    + " ----"
                    + Style.RESET_ALL
                )
            print(
                Fore.WHITE
                + Style.BRIGHT
                + "Points gagnés: "
                + str(player.points)
                + Style.RESET_ALL
            )
            Object_view.view_player(player)

    @staticmethod
    def view_additional_options(id, end=False):
        """
        ----- {id} -----
        En créer un nouveau
        and/or
        ----- {id} -----
        Fin de l'ajout
        """
        id_as_string = str(id)
        print(
            Fore.CYAN
            + "-----  "
            + id_as_string
            + "  -----"
            + "\nEn créer un nouveau"
            + Style.RESET_ALL
        )
        if end:
            id_as_string = str(id + 1)
            print(
                Fore.RED
                + "-----  "
                + id_as_string
                + "  -----"
                + "\nFin de l'ajout"
                + Style.RESET_ALL
            )

    @staticmethod
    def view_round_status(is_finished: bool, id: str, round_amount: int = 0):
        """
        --------- {id} ---------
        Statut de la ronde : Terminée
        or
        Statut de la ronde : En cours
        """
        print(
            Fore.CYAN + "---------",
            id,
            "/",
            round_amount,
            "---------",
            Style.RESET_ALL,
        )
        if is_finished:
            print(
                Fore.GREEN + "Statut de la ronde : Terminée", Style.RESET_ALL
            )
        else:
            print(Fore.RED + "Statut de la ronde : En cours", Style.RESET_ALL)

    @staticmethod
    def view_play_round(id: str):
        """
        ------ {id} -------
        Résusltats des matchs:
        1 - Victoire du joueur 1:
        2 - Victoire du joueur 2:
        D - Match nul:
        R - Retour:
        """
        print(Fore.CYAN + f"------ {id} -------", Style.RESET_ALL)
        print(Fore.YELLOW + "Résusltats des matchs:", Style.RESET_ALL)
        print(Fore.WHITE + "1 - Victoire du joueur 1", Style.RESET_ALL)
        print(Fore.BLUE + "2 - Victoire du joueur 2", Style.RESET_ALL)
        print(Fore.MAGENTA + "D - Match nul", Style.RESET_ALL)
        print(Fore.RED + "R - Retour\n", Style.RESET_ALL)
