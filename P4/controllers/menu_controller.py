from controllers.db_controller import Database
from controllers.manager_controller import Manager
from models.players import Player
from models.tournament import Tournament
from views.menu_view import *


class MainMenu:
    def __init__(self) -> None:
        print_main = Menus.main_menu()

    def select(self, selector: int):
        while True:
            try:
                if selector == "1":
                    play_tournament = 1
                elif selector == "2":
                    player_menu = PlayerMenu()
                    option_player = player_menu.select(
                        input("Selection : "))
                elif selector == "3":
                    tournament_management = TournamentMenu()
                    option_tournament = tournament_management.select(
                        input("Selection : "))
                elif selector == "4":
                    exit()
                else:
                    print("Cette option n'existe pas, veuillez réessayer")
                    return_back = MainMenu()
                    main_menu_selector = return_back.select(
                    input("Entrez votre réponse : "))
            except TypeError:
                print("You have entered a wrong selector Main Menu")


class PlayerMenu:
    def __init__(self) -> None:
        print_playermenu = Menus.players_menu()

    def select(self, selector: int):
        while True:
            # try:
                if selector == "1":
                    add_player = PlayerCreation()
                    new_player = add_player.create_new()
                elif selector == "2":
                    view_players = 2
                elif selector == "3":
                    return_back = MainMenu()
                    main_menu_selector = return_back.select(
                        input("Entrez votre réponse : "))
                else:
                    print("Cette option n'est pas disponible, veuillez réessayer")
                    return_back = MainMenu()
                    main_menu_selector = return_back.select(
                    input("Entrez votre réponse : "))
            # except TypeError:
            #     print("Vous avez entré un mauvais sélecteur Player Menu")
            #     PlayerMenu()
            #     return


class PlayerCreation:
    def __init__(self, players_list=[]) -> None:

        self.players_list: list[Player] = players_list 
        PlayerCreationView.player_creation() 
        
    def create_new(self):
            first_name = input("Prénom : ")
            last_name = input("Nom : ")
            birthdate = input("Date de naissance (jj/mm/aaaa) : ")
            gender = input("Genre (H/F/Na) : ")
            rank = input("Classement : ")
            ##Controle des inputs
            new_player = Player(first_name, last_name, birthdate, gender, rank)
            self.players_list.append(new_player)
            if len(self.players_list)<8:
                print("Le joueur a bien été ajouté", self.players_list)
                answer = PlayerCreation.yes_or_no(PlayerCreationView.ask_again().format(len(self.players_list)))
                # answer no
                if answer == 1:
                    self.create_new()
                else:
                    player_dict=Manager.player_list_fiting_db(self.players_list)
                    print("un ptit texte")
                    saving_list=Database.export_to_db(player_dict,"players")
                    PlayerMenu()
            else:
                player_dict=Manager.player_list_fiting_db(self.players_list)
                Database.export_to_db(player_dict,"players")
                MainMenu()
                
        
    def yes_or_no(question):
        answer = input(question + "(O/n): ").lower().strip()
        print("")
        while not(answer == "o" or answer == "oui" or \
        answer == "n" or answer == "non"):
            print("Entrez oui ou non")
            answer = input(question + "(O/n):").lower().strip()
            print("")
        if answer[0] == "o":
            return 1
        else:
            return 0        




class TournamentMenu:
    def __init__(self) -> None:
        print_tournament_menu=Menus.tournament_menu()
    
    def select(self,selector:int):
        while True:
            try:
                if selector == "1":
                    start_tournament=1
                elif selector == "2":
                    create_tournament=2
                elif selector == "3":
                    return_back = MainMenu()
                    main_menu_selector = return_back.select(
                        input("Entrez votre réponse : "))
                else:
                    print("Cette option n'est pas disponible, veuillez réessayer")
            except TypeError:
                print("Mauvais sélecteur")
                
                
class TournamentCreation:
    def __init__(self) -> None:
        print_title=TournamentCreationView.tournament_creation()

    def create_new(self):
        n=input("Nom : ")
        l=input("Localisation : ")
        dd=input("Date de début : ")
        df=input("Date de fin : ")
        tc=input("Controle de temps : ")
        rm=input("Nombre de tours (4 par défaut) : ")
        d=input("Description : ")
        self.new_tournament=Tournament(n,l,dd,df,tc,d,[],rm,[])
        
    def add_players_list(self,players_list:list):
        self.new_tournament.players=players_list