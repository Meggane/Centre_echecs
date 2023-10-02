import datetime
import sys

sys.path.append("..")
from model import model
from view import manually_retrieve_information

NUMBER_OF_ROUNDS = 4


class TournamentInformation:
    def __int__(self, tournament_name, tournament_place, tournament_start_date, tournament_end_date,
                current_round_number, round_list, list_of_registred_players,
                general_remarks_from_the_tournament_director):
        self.tournament_name = tournament_name
        self.tournament_place = tournament_place
        self.tournament_start_date = tournament_start_date
        self.tournament_end_date = tournament_end_date
        self.round_number = NUMBER_OF_ROUNDS
        self.current_round_number = current_round_number
        self.round_list = round_list
        self.list_of_registred_players = list_of_registred_players
        self.general_remarks_from_the_tournament_director = general_remarks_from_the_tournament_director

    def recovery_of_tournament_information(self):
        """Recovery of tournament information entered by the user"""
        self.tournament_name = input("Nom du tournoi : ")
        self.tournament_place = input("Lieu du tournoi : ")
        ask_tournament_start_date = input("Date de début du tournoi : ")
        try:
            if datetime.datetime.strptime(ask_tournament_start_date, "%d/%m/%Y"):
                self.tournament_start_date = ask_tournament_start_date
        except ValueError:
            print("La date de début du tournoi n'est pas au format JJ/MM/AAAA. Veuillez réessayer")
        ask_tournament_end_date = input("Date de fin du tournoi : ")
        try:
            if datetime.datetime.strptime(ask_tournament_end_date, "%d/%m/%Y"):
                self.tournament_end_date = ask_tournament_end_date
        except ValueError:
            print("La date de fin du tournoi n'est pas au format JJ/MM/AAAA. Veuillez réessayer")
        self.general_remarks_from_the_tournament_director = input("Description : ")
        return self.tournament_name, self.tournament_place, self.tournament_start_date, self.tournament_end_date, \
            self.general_remarks_from_the_tournament_director

    def players_that_can_be_added_to_the_tournament(self):
        """Creation of the menu to manually select the players to add to the tournament.

        The user enters the number corresponding to the desired player.
        """
        json_players_file = model.Model().json_file_playback("players.json")
        players_list = []
        for player in json_players_file.values():
            players_list.append(f"{player['Nom de famille']} {player['Prénom']} {player['Date de naissance']}")
        menu_number = 1
        print("Sélectionnez les joueurs à ajouter au tournoi (sélectionnez 6 joueurs minimum et un nombre pair) :")
        for player_index in range(len(players_list)):
            print(f"{menu_number}. {players_list[player_index]}")
            menu_number += 1

    def selection_of_players_to_add(self):
        """Recovery of players to add to the tournament according to the method menu
        players_that_can_be_added_to_the_tournament.
        """
        list_of_added_players = []
        while manually_retrieve_information.ManuallyRetrieveInformation().adding_a_new_player() == "o":
            self.players_that_can_be_added_to_the_tournament()
            players_to_add = input("Numéro du joueur à ajouter : ")
            list_of_added_players.append(players_to_add)
        return list_of_added_players
