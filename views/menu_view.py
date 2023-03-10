from colorama import Fore, Style
from utils import clear_console


class Menus_views:
    @staticmethod
    def main_menu():
        print("CHESSER π\n")
        print(Fore.CYAN + "Menu principal π’\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Jouer un tournoi π" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Gestion des joueurs π€" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Gestion des tournois π" + Style.RESET_ALL)
        print(Fore.YELLOW + "4. Afficher les classements π" + Style.RESET_ALL)
        print(Fore.RED + "5. Quitter β" + Style.RESET_ALL)

    @staticmethod
    def players_menu():
        print("CHESSER π\n")
        print(Fore.CYAN + "Menu joueurs π€\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. CrΓ©er un nouveau joueur β¨" + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + "2. Afficher la liste des joueurs π"
            + Style.RESET_ALL
        )
        print(Fore.RED + "3. Retour π" + Style.RESET_ALL)

    @staticmethod
    def tournament_menu():
        print("CHESSER π\n")
        print(Fore.CYAN + "Menu tournois π\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Jouer un tournoi π" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. CrΓ©er un tournoi β¨" + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + "3. Afficher la liste des tournois π"
            + Style.RESET_ALL
        )
        print(Fore.RED + "4. Retour π" + Style.RESET_ALL)

    @staticmethod
    def play_tournament_menu():
        print("CHESSER π\n")
        print(Fore.CYAN + "Menu lancement du tournois π\n" + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + "1. Ajouter des joueurs a un tournois π"
            + Style.RESET_ALL
        )
        print(Fore.YELLOW + "2. Jouer une Ronde π" + Style.RESET_ALL)
        print(Fore.RED + "3. Retour π" + Style.RESET_ALL)

    @staticmethod
    def tournament_submenu():
        print(Fore.CYAN + "Menu tournoi π\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Voir les joueurs π" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Voir les matchs π" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Supprimer le tournois π" + Style.RESET_ALL)
        print(Fore.RED + "4. Retour π" + Style.RESET_ALL)


class PlayerCreationView:
    @staticmethod
    def player_creation():
        print("CrΓ©ation d'un nouveau joueur β¨")

    @staticmethod
    def ask_again():
        return "\nVoulez-vous crΓ©er un nouveau joueur?\n({}/8 joueurs crΓ©Γ©s)"


class TournamentCreationView:
    @staticmethod
    def tournament_creation():
        clear_console()
        print(
            Fore.YELLOW + "CrΓ©ation d'un nouveau Tournois β¨" + Style.RESET_ALL
        )
