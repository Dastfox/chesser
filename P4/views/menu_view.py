
class Menus:

    def main_menu():
        print("CHESSER - Menu principal")
        print("1- Jouer un tournoi")
        print("2- Gestion des joueurs")
        print("3- Gestion des tournois")
        print("4- Quitter")

    def players_menu():
        print("CHESSER - Menu joueurs")
        print("1- Créer un nouveau joueur")
        print("2- Afficher la liste des joueurs")
        print("3- Retour")

    def tournament_menu():
        print("CHESSER - Menu tournois")
        print("1- Jouer un tournoi")
        print("2- Créer un tournoi")
        print("3- Retour")


class PlayerCreationView:

    def player_creation():
        print("Création d'un nouveau joueur")

    def ask_again():
        return "Voulez-vous créer un nouveau joueur?\n({}/8 joueurs créés)"

class TournamentCreationVinew:

    def tournament_creation():
        print("Création d'un nouveau Tournoi")