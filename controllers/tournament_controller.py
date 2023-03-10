import time
from controllers.player_controller import PlayerCreation
from models.round import Round
from views.object_view import Object_view
from controllers.db_controller import Database
from controllers.manager_controller import Manager
from models.tournament import Tournament, serialize_tournament
from models.players import Player
from views.menu_view import TournamentCreationView

from utils import clear_console
from controllers.list_controller import view_list
from utils import yes_or_no

"""
leaderboard
"""


class Leaderboard:
    def __init__(
        self,
        tournament: Tournament | None = None,
    ) -> None:
        clear_console()
        print("Leaderboard", tournament)
        selected_tournament = None
        while not (
            type(selected_tournament) is Tournament
            or selected_tournament == "back"
        ):
            if tournament:
                selected_tournament = tournament
            else:
                selected_tournament = view_list(
                    TournamentCreation,
                    Tournament,
                    True,
                    "Sélectionnez un tournoi pour afficher son leaderboard",
                    False,
                    False,
                    tournament_can_display_leaderbord,
                )
        if selected_tournament == "back":
            return
        if isinstance(selected_tournament, Tournament):
            players = selected_tournament.players
            if len(players) == 0:
                clear_console()
                print("Aucun joueur n'a été ajouté à ce tournoi")
                input("Appuyez sur Entrée pour continuer...")
                return
            players.sort(key=lambda x: x.points, reverse=True)
            clear_console()
            Object_view.view_leaderboard(players)
            input("Appuyez sur Entrée pour continuer...")
        else:
            print("Erreur : Le tournoi sélectionné n'est pas valide")
            input("Appuyez sur Entrée pour continuer...")
            return


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
        selected_tournament = view_list(
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

        The user will be prompted to enter the name,
        location, start and end dates, time control,
        round amount, and description of the tournament.
         These values will be used to create a new
        Tournament object, which will then be added
        to the database.
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
        rounds = []

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

        # Prompt the user to enter the start
        # and end dates of the tournament
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
        time_control = input(
            "Controle de temps \n(blitz, bullet ou coup rapide): "
        )

        # Prompt the user to enter the round amount
        # for the tournament (default is 4)
        while not type(round_amount) is int:
            if round_amount != "":
                print("Veuillez entrer un nombre de tours valide")
            round_amount = int(input("Nombre de tours (4 par défaut) : "))
            if round_amount == "":
                round_amount = 4

        # Prompt the user to enter a description for the tournament
        description = input("Description : ")

        # Format the date range as a string
        date = f"{date_start} - {date_end}"

        # Create a new Tournament object with the user-provided values
        new_tournament = Tournament(
            name,
            location,
            date,
            round_amount,
            rounds,
            players,
            time_control,
            description,
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
            if (
                tournament is None
                or tournament != "back"
                or tournament is not Tournament
            ):
                return
            else:
                print("Pas de tournois")
                return
        if tournament == "back":
            return

        print(tournament, "sélectionné")
        players: list[Player] = self.select_players()
        print(players, "players")
        for player in players:
            player.points = 0

        if not isinstance(tournament, Tournament):
            return

        for player_in_t in tournament.players:
            if player_in_t not in players:
                players.append(player_in_t)

        tournament.players = players
        tournament_db = serialize_tournament(tournament)
        Database.update_db_object(
            tournament.name, tournament_db, "tournaments"
        )

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
        clear_console()
        selected_players: list[Player] = []
        while True:
            new_player = None
            while not (isinstance(new_player, Player) or new_player == "end"):
                new_player = view_list(
                    PlayerCreation,
                    Player,
                    True,
                    "Sélectionnez un joueur par son identifiant : ",
                    True,
                    True,
                )
            if new_player == "end":
                return selected_players
            if new_player not in selected_players and isinstance(
                new_player, Player
            ):
                selected_players.append(new_player)

    def play_a_round(self, tournament: Tournament | None = None):
        selected_tournament = None
        while not (
            type(selected_tournament) is Tournament
            or selected_tournament == "back"
        ):
            if tournament is None:
                selected_tournament = self.select_tournament(
                    tournament_can_play
                )
            else:
                selected_tournament = tournament

        if selected_tournament == "back":
            return
        elif not isinstance(selected_tournament, Tournament):
            return
        if selected_tournament.rounds and len(selected_tournament.rounds) > 0:
            last_round: Round = selected_tournament.rounds[-1]
            if last_round.is_finished:
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
            Object_view.view_match(match_player, 0, True)
        number_of_matches = 0
        for match in round.matches:
            if match[2] not in ["1", "2", "d", "D"]:
                number_of_matches += 1
        print(f"{number_of_matches} matchs restants.")
        if yes_or_no("Jouer la ronde?"):
            clear_console()
            selected_tournament.play_round()

        tournament_serialized = serialize_tournament(selected_tournament)
        Database.update_db_object(
            selected_tournament.name,
            tournament_serialized,
            "tournaments",
        )
        if selected_tournament.rounds[-1].is_finished:
            if selected_tournament.round_amount == len(
                selected_tournament.rounds
            ):
                print("Tournois terminé")
                selected_tournament.update_ranks()
                tournament_serialized = serialize_tournament(
                    selected_tournament
                )
                Database.update_db_object(
                    selected_tournament.name,
                    tournament_serialized,
                    "tournaments",
                )
                Leaderboard(
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
    elif len(tournament.rounds) <= tournament.round_amount:
        if (
            len(tournament.rounds) == tournament.round_amount
            and tournament.rounds[-1].is_finished
        ):
            return False
        else:
            return True
    else:
        return False


def tournament_can_display_leaderbord(tournament: Tournament):
    if (
        not tournament.rounds
        or len(tournament.rounds) < int(tournament.round_amount)
        or not tournament.rounds[-1].is_finished
    ):
        return False
    return True
