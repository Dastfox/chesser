from colorama import Fore, Style

from models.players import Player

# from models.tournament import Tournament


class List_view:
    @staticmethod
    def view_player(player: Player, id: int = 0):
        id_as_str = str(id)
        rank_as_str = str(player.rank)
        if id != 0:
            print(Fore.YELLOW + "-----  " + id_as_str + "  -----" + Style.RESET_ALL)
        print(Fore.YELLOW + "\nPrénom :", player.first_name + Style.RESET_ALL)
        print(Fore.YELLOW + "Nom :", player.last_name + Style.RESET_ALL)
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
        print(Fore.YELLOW + "Classement :", rank_as_str + "🏆" + Style.RESET_ALL)

    @staticmethod
    def view_tournament(tournament, id: int = 0):
        round_as_str = str(tournament.round_amount)
        id_as_str = str(id)
        if id != 0:
            print(Fore.YELLOW + "-----  " + id_as_str + "  -----" + Style.RESET_ALL)
        print(Fore.YELLOW + "\nNom :", tournament.name + Style.RESET_ALL)
        print(
            Fore.YELLOW + "Localisation :", tournament.location + "🌍" + Style.RESET_ALL
        )
        print(Fore.YELLOW + "Date :", tournament.date + "📅" + Style.RESET_ALL)
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
            print(Fore.YELLOW + "-----  " + id_as_str + "  -----" + Style.RESET_ALL)
        print(
            Fore.WHITE + "Joueur blanc :",
            p1.first_name + " " + p1.last_name + Style.RESET_ALL,
            Fore.BLUE
            + "Joueur noir:"
            + p2.first_name
            + " "
            + p2.last_name
            + Style.RESET_ALL,
        )
        if print_reslut and result in ("1", "2", "D", "d"):
            if result == 1:
                print(
                    Fore.YELLOW + "Gagnant :",
                    p1.first_name + " " + p1.last_name + Style.RESET_ALL,
                )
            elif match.result == 2:
                print(
                    Fore.YELLOW + "Gagnant :",
                    p2.first_name + " " + p2.last_name + Style.RESET_ALL,
                )
            else:
                print(Fore.YELLOW + "Match nul" + Style.RESET_ALL)
