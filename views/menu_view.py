from colorama import Fore, Style
from utils import clear_console


class Menus_views:
    @staticmethod
    def main_menu():
        print("CHESSER 🏆\n")
        print(Fore.CYAN + "Menu principal 🔢\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Jouer un tournoi 🏆" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Gestion des joueurs 👤" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Gestion des tournois 🏆" + Style.RESET_ALL)
        print(Fore.YELLOW + "4. Afficher les classements 🏆" + Style.RESET_ALL)
        print(Fore.RED + "5. Quitter ❌" + Style.RESET_ALL)

    @staticmethod
    def players_menu():
        print("CHESSER 🏆\n")
        print(Fore.CYAN + "Menu joueurs 👤\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Créer un nouveau joueur ✨" + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + "2. Afficher la liste des joueurs 👀"
            + Style.RESET_ALL
        )
        print(Fore.RED + "3. Retour 🔙" + Style.RESET_ALL)

    @staticmethod
    def tournament_menu():
        print("CHESSER 🏆\n")
        print(Fore.CYAN + "Menu tournois 🏆\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Jouer un tournoi 🏆" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Créer un tournoi ✨" + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + "3. Afficher la liste des tournois 👀"
            + Style.RESET_ALL
        )
        print(Fore.RED + "4. Retour 🔙" + Style.RESET_ALL)

    @staticmethod
    def play_tournament_menu():
        print("CHESSER 🏆\n")
        print(Fore.CYAN + "Menu lancement du tournois 🏆\n" + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + "1. Ajouter des joueurs a un tournois 🏆"
            + Style.RESET_ALL
        )
        print(Fore.YELLOW + "2. Jouer une Ronde 🏆" + Style.RESET_ALL)
        print(Fore.RED + "3. Retour 🔙" + Style.RESET_ALL)

    @staticmethod
    def tournament_submenu():
        print(Fore.CYAN + "Menu tournoi 🏆\n" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Voir les joueurs 🏆" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Voir les matchs 🏆" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Supprimer le tournois 🏆" + Style.RESET_ALL)
        print(Fore.RED + "4. Retour 🔙" + Style.RESET_ALL)


class PlayerCreationView:
    @staticmethod
    def player_creation():
        print("Création d'un nouveau joueur ✨")

    @staticmethod
    def ask_again():
        return "\nVoulez-vous créer un nouveau joueur?\n({}/8 joueurs créés)"


class TournamentCreationView:
    @staticmethod
    def tournament_creation():
        clear_console()
        print(
            Fore.YELLOW + "Création d'un nouveau Tournois ✨" + Style.RESET_ALL
        )
