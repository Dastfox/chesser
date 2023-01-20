import json
import time
from controllers.player_controller import PlayerCreation
from models.round import Round
from views.lists_view import List_view
from controllers.db_controller import Database
from controllers.manager_controller import Manager
from models.tournament import Tournament, serialize_tournament
from views.menu_view import *
from utils import clear_console
from controllers.list_controller import view_list
from utils import yes_or_no

"""
leaderboard
"""


class Leaderboard:
    def __init__(
        self,
        tournament: Tournament = None,
    ) -> None:
        clear_console()
        print("Leaderboard", tournament)
        if tournament is None:
            selected_tournament = view_list(
                TournamentCreation,
                Tournament,
                True,
                "Sélectionnez un tournoi pour afficher son leaderboard",
                False,
                False,
                tournament_can_display_leaderbord,
            )
        else:
            selected_tournament = tournament
        players = selected_tournament.players
        if len(players) == 0:
            clear_console()
            print("Aucun joueur n'a été ajouté à ce tournoi")
            input("Appuyez sur Entrée pour continuer...")
            return
        players.sort(key=lambda x: x.points, reverse=True)
        clear_console()
        List_view.view_leaderboard(players)
        input("Appuyez sur Entrée pour continuer...")


"""
Tounaments
"""


class TournamentList:
    """A class representing the tournament list in a game.

    Attributes:
        None
    """

    def __init__(self):
        self.tournaments = []

    def view_list(self):
        """View the list of tournaments.

        Returns:
            None
        """
        clear_console()
        selected_tournament: Tournament = view_list(
            TournamentCreation,
            Tournament,
            True,
            question="Sélectionnez un tournoi pour afficher ses joueurs",
        )
        clear_console()
        return selected_tournament


class TournamentCreation:
    def __init__(self, tournament_list=[]) -> None:

        self.tournament_list: list[Tournament] = tournament_list
        TournamentCreationView.tournament_creation()

    @staticmethod
    def date_validator(date: str) -> bool:
        if len(date) != 8:
            return False
        if not date.isnumeric():
            return False
        day = int(date[0:2])
        month = int(date[2:4])
        year = int(date[4:8])
        if day < 1 or day > 31:
            return False
        if month < 1 or month > 12:
            return False
        if year < 1900 or year > 2078:
            return False
        return True

    def create_new(self):
        """
        Create a new tournament object and add it to the database.

        The user will be prompted to enter the name, location, start and end dates, time control,
        round amount, and description of the tournament. These values will be used to create a new
        Tournament object, which will then be added to the database.
        """
        # init variables
        name = ""
        location = ""
        date_start = ""
        date_end = ""
        date = ""
        time_control = ""
        description = ""
        round_amount = 4
        players = []
        turn = {}

        # Prompt the user to enter the name of the tournament
        while not name:
            if name != " ":
                print("Veuillez entrer un nom")
            name = input("Nom : ")

        # Prompt the user to enter the location of the tournament
        while not location:
            if location != " ":
                print("Veuillez entrer un lieu")
            location = input("Localisation : ")

        # Prompt the user to enter the start and end dates of the tournament
        while not TournamentCreation.date_validator(
            date_start
        ) or not TournamentCreation.date_validator(date_end):
            if date_start != "" and date_end != "" and date_start > date_end:
                print(
                    "Veuillez entrer une date de début et de fin valide",
                    date_start,
                    ">",
                    date_end,
                )
            while not TournamentCreation.date_validator(date_start):
                if date_start != "":
                    print("Veuillez entrer une date de début valide")
                date_start = input("Date de début : ")
            while not TournamentCreation.date_validator(date_end):
                if date_end != "":
                    print("Veuillez entrer une date de fin valide")
                date_end = input("Date de fin : ")

        # Prompt the user to enter the time control for the tournament
        time_control = input("Controle de temps \n(blitz, bullet ou coup rapide): ")

        # Prompt the user to enter the round amount for the tournament (default is 4)
        round_amount = input("Nombre de tours (4 par défaut) : ")

        if round_amount == "":
            round_amount = 4

        # Prompt the user to enter a description for the tournament
        description = input("Description : ")

        # Format the date range as a string
        date = f"{date_start} - {date_end}"

        # Create a new Tournament object with the user-provided values
        new_tournament = Tournament(
            name, location, date, round_amount, turn, players, time_control, description
        )

        # Add the new tournament to the database
        list = []
        list.append(new_tournament)
        tournament_dict = Manager.object_list_fitting_db(list)
        Database.export_to_db(tournament_dict, "tournaments")

        # Confirm that the tournament has been added to the database
        clear_console()
        print(new_tournament.name, "a été ajouté à la base de données")
        time.sleep(1)
        return new_tournament


"""
Play Tournament
"""


class PlayTournamentController:
    def add_players_to_tournament(self):
        clear_console()
        tournament = self.select_tournament()
        if tournament is None:
            create_new = yes_or_no("Aucun tournois trouvé. En créer un?")
            if create_new:
                tournament = self.create_tournament()
            if tournament is None:
                return
            else:
                print("Pas de tournois")
                return
        if tournament == "back":
            return

        players: list[Player] = self.select_players()
        for player in players:
            player.points = 0

        for player_in_t in tournament.players:
            if player_in_t not in players:
                players.append(player_in_t)

        tournament.players = players
        tournament_db = serialize_tournament(tournament)
        Database.update_db_object(tournament.name, tournament_db, "tournaments")

        clear_console()
        print(len(players), "joueur ajoutés au tournois")
        time.sleep(3)

    def select_tournament(self, tournament_has_players=None):
        selected_tournament = view_list(
            TournamentCreation,
            Tournament,
            True,
            "\n\nSélectionnez un tournois: ",
            True,
            False,
            tournament_has_players,
        )
        return selected_tournament

    def create_tournament(self):
        tournament_creation = TournamentCreation()
        tournament_creation.create_new()

    def select_players(self):
        # players = Database.read_db("players")
        selected_players: list[Player | Tournament] = []
        while True:
            new_player = view_list(
                PlayerCreation,
                Player,
                True,
                "Sélectionnez un joueur par son identifiant : ",
                True,
                True,
            )
            if new_player != "End":
                selected_players.append(new_player)
            else:
                return selected_players

    def play_a_round(self, tournament: Tournament = None):
        if tournament is None:
            selected_tournament: Tournament = self.select_tournament(
                tournament_can_play
            )
            if selected_tournament == "back":
                return
        else:
            selected_tournament = tournament

        if selected_tournament.rounds and len(selected_tournament.rounds) > 0:
            last_round: Round = selected_tournament.rounds[-1]
            if last_round.is_finished == True:
                last_round = selected_tournament.generate_pairs()
        else:
            last_round = selected_tournament.generate_pairs()

        round = last_round

        clear_console()
        print(f"------ {round.id} -------\n")
        for match in round.matches:
            match_player = [
                Player.deserialize_players([match[0]])[0],
                Player.deserialize_players([match[1]])[0],
                match[2],
            ]
            List_view.view_match(match_player)

        if yes_or_no("Jouer la ronde?"):
            clear_console()
            selected_tournament.play_round()

        tournament_serialized = serialize_tournament(selected_tournament)
        Database.update_db_object(
            selected_tournament.name,
            tournament_serialized,
            "tournaments",
        )
        if selected_tournament.rounds[-1].is_finished == True:
            if selected_tournament.round_amount == len(selected_tournament.rounds):
                print("Tournois terminé")
                selected_tournament.update_ranks()
                tournament_serialized = serialize_tournament(selected_tournament)
                Database.update_db_object(
                    selected_tournament.name, tournament_serialized, "tournaments"
                )
                leaderboard = Leaderboard(
                    selected_tournament,
                )
            elif yes_or_no("Générer les matchups pour une autre ronde?"):
                clear_console()
                self.play_a_round(selected_tournament)


def tournament_can_play(tournament: Tournament):
    if not tournament.players or len(tournament.players) < 1:
        return False
    elif not tournament.rounds and len(tournament.rounds) == 0:
        return True
    elif (
        len(tournament.rounds) <= tournament.round_amount
        and tournament.rounds[-1].is_finished == True
    ):
        return True
    else:
        return False


def tournament_can_display_leaderbord(tournament: Tournament):
    if (
        not tournament.rounds
        or len(tournament.rounds) < int(tournament.round_amount)
        or tournament.rounds[-1].is_finished == False
    ):
        return False
    return True
