import datetime
import re
import sys

sys.path.append("..")
from model import model
from view import manually_retrieve_information

NUMBER_OF_ROUNDS = 4


class TournamentInformation:
    def __init__(self):
        self.tournament_information = []

    def recovery_of_tournament_information(self):
        """Recovery of tournament information entered by the user"""
        tournament_name_is_correct = False
        tournament_name = None
        while tournament_name_is_correct is False:
            tournament_name = input("Nom du tournoi : ")
            if re.findall(r"[^a-zA-Z-\s0-9éèîïÉ+]", tournament_name) or len(tournament_name) < 2:
                print("Le nom du tournoi n'est pas correct. Veuillez réessayer")
            else:
                tournament_name_is_correct = True
        tournament_place_is_correct = False
        tournament_place = None
        while tournament_place_is_correct is False:
            tournament_place = input("Lieu du tournoi : ")
            if re.findall(r"[^a-zA-Z-\s0-9éèîïÉ+]", tournament_place) or len(tournament_place) < 2:
                print("Le lieu du tournoi n'est pas correct. Veuillez réessayer")
            else:
                tournament_place_is_correct = True
        while True:
            tournament_start_date = input("Date de début du tournoi : ")
            try:
                datetime.datetime.strptime(tournament_start_date, "%d/%m/%Y")
                break
            except ValueError:
                print("La date de début du tournoi n'est pas au format JJ/MM/AAAA. Veuillez réessayer")
        while True:
            tournament_end_date = input("Date de fin du tournoi : ")
            try:
                datetime.datetime.strptime(tournament_end_date, "%d/%m/%Y")
                break
            except ValueError:
                print("La date de fin du tournoi n'est pas au format JJ/MM/AAAA. Veuillez réessayer")
        general_remarks_from_the_tournament_director = input("Description : ")
        self.tournament_information.append(tournament_name)
        self.tournament_information.append(tournament_place)
        self.tournament_information.append(tournament_start_date)
        self.tournament_information.append(tournament_end_date)
        self.tournament_information.append(general_remarks_from_the_tournament_director)
        return self.tournament_information

    def players_that_can_be_added_to_the_tournament(self):
        """Creation of the menu to manually select the players to add to the tournament.

        The user enters the number corresponding to the desired player.
        """
        json_players_file = model.Model().json_file_playback("players.json")
        players_list = []
        display_of_the_selection_of_tournament_players = []
        for player in json_players_file.values():
            players_list.append(f"{player['Nom de famille']} {player['Prénom']} {player['Date de naissance']}")
        menu_number = 1
        display_of_the_selection_of_tournament_players.append("Sélectionnez les joueurs à ajouter au tournoi ("
                                                              "sélectionnez 6 joueurs minimum et un nombre pair) :")
        for player_index in range(len(players_list)):
            display_of_the_selection_of_tournament_players.append(f"{menu_number}. {players_list[player_index]}")
            menu_number += 1
        return display_of_the_selection_of_tournament_players

    def selection_of_players_to_add(self):
        """Recovery of players to add to the tournament according to the method menu
        players_that_can_be_added_to_the_tournament.
        """
        list_of_added_players = []
        while manually_retrieve_information.ManuallyRetrieveInformation().adding_a_new_player() == "o":
            for selection_to_display in self.players_that_can_be_added_to_the_tournament():
                print(selection_to_display)
            players_to_add = input("Numéro du joueur à ajouter : ")
            list_of_added_players.append(players_to_add)
        return list_of_added_players
