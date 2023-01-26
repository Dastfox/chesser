from colorama import Fore, Style, Back

from models.players import Player


class List_view:
    @staticmethod
    def view_player(player: Player, id: int = 0):
        id_as_str = str(id)
        rank_as_str = str(player.rank)
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
        print(
            Fore.YELLOW + "Classement :", rank_as_str + Style.RESET_ALL + "\n"
        )

    @staticmethod
    def view_tournament(tournament, id: int = 0):
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
            print(
                Fore.WHITE
                + Style.BRIGHT
                + "Points gagnés: "
                + str(player.points)
                + Style.RESET_ALL
            )
            List_view.view_player(player)
