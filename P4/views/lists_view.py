from colorama import Fore, Style

from models.players import Player
from models.tournament import Tournament


class List_view:
    @staticmethod
    def view_player(player: Player, id: int = 0):
        id_as_str = str(id)
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
        print(Fore.YELLOW + "Genre :", player.gender + Style.RESET_ALL)
        print(Fore.YELLOW + "Classement :", player.rank + "🏆" + Style.RESET_ALL)

    @staticmethod
    def view_tournament(tournament: Tournament, id: int = 0):
        round_as_str = str(tournament.round_amount)
        id_as_str = str(id)
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
        if tournament.players and len(tournament.players) > 0:
            for player in tournament.players:
                print(
                    Fore.YELLOW + "Joueurs :",
                    player.first_name + player.last_name + "👤" + Style.RESET_ALL,
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
