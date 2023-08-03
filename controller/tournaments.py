import re
import os
import sys

sys.path.append("..")
from view import tournament_information
from model import model


class Tournaments:
    def __init__(self):
        pass

    def creation_of_tournament(self):
        """Tournament creation.

        Each tournament has a number and the information collected from the user.
        The number of rounds is set by default to 4.
        Only the current round number and the list of rounds will change throughout the tournament.
        """
        tournament_number = 1
        if os.path.isfile("../data/tournaments/tournaments.json"):
            json_tournaments_file = model.Model().json_file_playback("tournaments.json")
            list_of_number_of_each_tournament = []
            for number_of_each_tournament in json_tournaments_file:
                retrieving_the_number_only = re.findall(r"[0-9]+", number_of_each_tournament)
                list_of_number_of_each_tournament.extend(list(map(int, retrieving_the_number_only)))
            number_of_the_last_tournament = list_of_number_of_each_tournament[-1]
            number_of_the_last_tournament += 1
            tournament_number = number_of_the_last_tournament

        list_of_tournament_information = []
        for each_information_of_the_tournament \
                in tournament_information.TournamentInformation().recovery_of_tournament_information():
            list_of_tournament_information.append(each_information_of_the_tournament)
        number_of_rounds_of_the_tournament = tournament_information.NUMBER_OF_ROUNDS

        json_players_file = model.Model().json_file_playback("players.json")
        list_of_players_in_json_file = []
        for player_number, player_information in json_players_file.items():
            list_of_players_in_json_file.append(f"{player_number} : {player_information['Nom de famille']} "
                                                f"{player_information['Prenom']}")

        list_of_players_to_add = tournament_information.TournamentInformation().selection_of_players_to_add()
        list_of_numbers_of_players_participating_in_the_tournament = list(map(int, list_of_players_to_add))
        liste_tournoi_players = []
        for list_index in range(len(list_of_players_in_json_file)):
            for number_of_player_participating_in_the_tournament \
                    in list_of_numbers_of_players_participating_in_the_tournament:
                if list_index == number_of_player_participating_in_the_tournament - 1:
                    liste_tournoi_players.append(list_of_players_in_json_file[list_index])

        tournament_information_to_be_created = {
            f"Tournoi numero {tournament_number}": {
                "Nom du tournoi": list_of_tournament_information[0],
                "Lieu du tournoi": list_of_tournament_information[1],
                "Date de debut du tournoi": list_of_tournament_information[2],
                "Date de fin du tournoi": list_of_tournament_information[3],
                "Nombre de tour": number_of_rounds_of_the_tournament,
                "Numero du tour actuel": 1,
                "Liste des tours": "En attente",
                "Liste des joueurs": liste_tournoi_players,
                "Description": list_of_tournament_information[4]
            }
        }

        if os.path.isfile("../data/tournaments/tournaments.json"):
            json_tournaments_file = model.Model().json_file_playback("tournaments.json")
            json_tournaments_file.update(tournament_information_to_be_created)
            model.Model().json_file_creation("tournaments.json", json_tournaments_file)
        else:
            model.Model().json_file_creation("tournaments.json", tournament_information_to_be_created)
