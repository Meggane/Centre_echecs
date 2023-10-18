import re
import sys

sys.path.append("..")
from controller import players
from model import model


class Reports:
    def __init__(self):
        self.display_from_the_list_of_players_in_column = []
        self.display_from_the_list_of_tournaments_in_column = []
        self.items_to_display = []

    def list_of_players_in_alphabetical_order(self):
        """Display the list of players in alphabetical order by last name."""
        try:
            list_of_players_in_alphabetical_order = players.Players().sort_players_alphabetically()
            list_of_all_players = []
            self.display_from_the_list_of_players_in_column.append("\nLISTE DE TOUS LES JOUEURS PAR ORDRE ALPHABÉTIQUE"
                                                                   " :")
            for player in list_of_players_in_alphabetical_order:
                list_of_all_players.append(player)
            self.display_from_the_list_of_players_in_column.append("\n".join(list_of_all_players))
        except FileNotFoundError:
            self.display_from_the_list_of_players_in_column.append("Le fichier demandé n'existe pas")
        return self.display_from_the_list_of_players_in_column

    def list_of_all_tournaments(self):
        """Display the list of all tournaments with all related information."""
        try:
            json_file_tournaments = model.Model().json_file_playback("tournaments.json")
            tournaments_list = []
            self.display_from_the_list_of_tournaments_in_column.append("\n\nLISTE DE TOUS LES TOURNOIS : \n\n")
            for tournament_number, tournament_information in json_file_tournaments.items():
                tournaments_list.append(tournament_number.upper())
                for wording in tournament_information:
                    match wording:
                        case "Liste des tours":
                            tournaments_list.append(f"\n{wording}: ".upper())
                            # Check if the tournament has not started yet
                            if type(tournament_information["Liste des tours"]) == str:
                                tournaments_list.append(tournament_information["Liste des tours"])
                            else:
                                for tournament_round, tournament_round_information in \
                                        tournament_information["Liste des tours"].items():
                                    tournaments_list.append(f"\n{tournament_round.upper()}")
                                    for dictionary_key, dictionary_value in tournament_round_information.items():
                                        if dictionary_key == "Couleur des pièces des joueurs des matchs":
                                            tournaments_list.append(f"{dictionary_key}: ")
                                            for player_number, color in dictionary_value.items():
                                                tournaments_list.append(f"{player_number}: {color}")
                                        else:
                                            tournaments_list.append(f"{dictionary_key}: {dictionary_value}")
                        case "Liste des joueurs":
                            tournaments_list.append(f"\n{wording}: ".upper())
                            for player, score in tournament_information["Liste des joueurs"].items():
                                tournaments_list.append(f"{player}: {score}")
                        case _:
                            if wording == "Description":
                                tournaments_list.append(f"\n{wording}: {tournament_information[f'{wording}']}")
                            else:
                                tournaments_list.append(f"{wording}: {tournament_information[f'{wording}']}")
                tournaments_list.append("\n")
                self.display_from_the_list_of_tournaments_in_column.append("\n".join(tournaments_list))
        except FileNotFoundError:
            self.display_from_the_list_of_tournaments_in_column.append("Le fichier demandé n'existe pas")
        return self.display_from_the_list_of_tournaments_in_column

    def name_and_date_of_a_given_tournament(self, tournament_name):
        """Display the name and date of the chosen tournament."""
        try:
            json_file_tournaments = model.Model().json_file_playback("tournaments.json")
            if self.check_tounament_names(tournament_name) is True:
                for tournament_information in json_file_tournaments.values():
                    self.items_to_display.append(f"\nNom du tournoi: {tournament_name}")
                    self.items_to_display.append(f"Date de début du tournoi: "
                                                 f"{tournament_information['Date de début du tournoi']}")
                    self.items_to_display.append(f"Date de fin du tournoi: "
                                                 f"{tournament_information['Date de fin du tournoi']}")
            else:
                self.items_to_display.append("Le tournoi sélectionné n'existe pas")
        except FileNotFoundError:
            self.items_to_display.append("Le fichier demandé n'existe pas")
        return self.items_to_display

    def list_of_players_in_a_given_tournament(self, tournament_name):
        """Display the family and first names of players in a given tournament. Players are sorted alphabetically."""
        try:
            json_file_tournaments = model.Model().json_file_playback("tournaments.json")
            if self.check_tounament_names(tournament_name) is True:
                for tournament_information in json_file_tournaments.values():
                    self.items_to_display.append(f'\nLISTE DES JOUEURS DU TOURNOI "{tournament_name.upper()}": ')
                    list_of_players = []
                    for player in tournament_information["Liste des joueurs"]:
                        recovery_of_the_players_family_and_first_names = re.findall(r"[A-Za-z- ]+", player)
                        family_name = recovery_of_the_players_family_and_first_names[-2]
                        first_name = recovery_of_the_players_family_and_first_names[-1]
                        list_of_players.append(f"{family_name} {first_name}")
                    sorting_of_players = sorted(list_of_players)
                    for player_in_alphabetical_order in sorting_of_players:
                        self.items_to_display.append(player_in_alphabetical_order)
            else:
                self.items_to_display.append("Le tournoi sélectionné n'existe pas")
        except FileNotFoundError:
            self.items_to_display.append("Le fichier demandé n'existe pas")
        return self.items_to_display

    def rounds_and_matches_of_a_given_tournament(self, tournament_name):
        """Display the list of all rounds of the tournament and all matches of the round.

        We find the players' scores, the start and end date and time as well as the color of the pieces used by the
        players.
        """
        try:
            json_file_tournaments = model.Model().json_file_playback("tournaments.json")
            if self.check_tounament_names(tournament_name) is True:
                for tournament_information in json_file_tournaments.values():
                    self.items_to_display.append(f'\nLISTE DES TOURS DU TOURNOI "{tournament_name.upper()}": \n')
                    if type(tournament_information["Liste des tours"]) == dict:
                        for round_number, round_information in tournament_information["Liste des tours"].items():
                            self.items_to_display.append(round_number.upper())
                            for wording, indication_of_the_wording in round_information.items():
                                if wording == "Couleur des pièces des joueurs des matchs":
                                    self.items_to_display.append(f"{wording}: ")
                                    for player_number, color_of_the_pieces in indication_of_the_wording.items():
                                        self.items_to_display.append(f"{player_number}: {color_of_the_pieces}")
                                else:
                                    self.items_to_display.append(f"{wording}: {indication_of_the_wording}")
                            self.items_to_display.append("\n")
                    else:
                        self.items_to_display.append(tournament_information["Liste des tours"])
            else:
                self.items_to_display.append("Le tournoi sélectionné n'existe pas")
        except FileNotFoundError:
            self.items_to_display.append("Le fichier demandé n'existe pas")
        return self.items_to_display

    def check_tounament_names(self, name_of_the_selected_tournament):
        """We check if the tournament name exists in the list of all tournaments.

        If it exists we return True otherwise False.
        """
        json_tournaments_file = model.Model().json_file_playback("tournaments.json")
        the_tournament_exists = False
        for tournament_information in json_tournaments_file.values():
            if name_of_the_selected_tournament == tournament_information["Nom du tournoi"]:
                the_tournament_exists = True
        return the_tournament_exists
