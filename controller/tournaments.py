import re
import os
import sys

sys.path.append("..")
from view import tournament_information
from model import model
from controller import matches


class Tournaments:
    def __init__(self):
        self.tournament_information_to_be_created = {}

    def creation_of_tournament(self, score=0):
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
        list_of_player_number = []
        for player_number, player_information in json_players_file.items():
            list_of_players_in_json_file.append(f"{player_number} / {player_information['Nom de famille']} "
                                                f"{player_information['Prenom']}")
            list_of_player_number.extend(re.findall(r"[0-9]+", player_number))

        list_of_players_to_add = tournament_information.TournamentInformation().selection_of_players_to_add()
        if len(list_of_players_to_add) < 6:
            print("Vous n'avez pas ajouté suffisamment de participant. Veuillez réessayer.")
        elif len(list_of_players_to_add) % 2 != 0:
            print("Le nombre de participant n'est pas pair. Veuillez réessayer.")
        else:
            player_number_added_incorrect = False
            for num in list_of_players_to_add:
                if num not in list_of_player_number:
                    print("Un numéro de joueur sélectionné n'existe pas. Veuillez réessayer.")
                    player_number_added_incorrect = True
            list_of_numbers_of_players_participating_in_the_tournament = list(map(int, list_of_players_to_add))
            liste_tournoi_players = []
            for list_index in range(len(list_of_players_in_json_file)):
                for number_of_player_participating_in_the_tournament \
                        in list_of_numbers_of_players_participating_in_the_tournament:
                    if list_index == number_of_player_participating_in_the_tournament - 1:
                        liste_tournoi_players.append(list_of_players_in_json_file[list_index])

            list_of_players_of_the_tournament_with_their_score = {}
            for index_of_each_player_in_json_players_file in range(len(list_of_players_in_json_file)):
                for player_number_in_the_tournament in list_of_numbers_of_players_participating_in_the_tournament:
                    if index_of_each_player_in_json_players_file == player_number_in_the_tournament - 1:
                        list_of_players_of_the_tournament_with_their_score.update({
                            list_of_players_in_json_file[index_of_each_player_in_json_players_file]: score
                        })

            self.tournament_information_to_be_created.update({
                f"Tournoi numero {tournament_number}": {
                    "Nom du tournoi": list_of_tournament_information[0],
                    "Lieu du tournoi": list_of_tournament_information[1],
                    "Date de debut du tournoi": list_of_tournament_information[2],
                    "Date de fin du tournoi": list_of_tournament_information[3],
                    "Nombre de tour": number_of_rounds_of_the_tournament,
                    "Numero du tour actuel": 1,
                    "Liste des tours": "En attente",
                    "Liste des joueurs": list_of_players_of_the_tournament_with_their_score,
                    "Description": list_of_tournament_information[4]
                }
            })
            if player_number_added_incorrect is False:
                if os.path.isfile("../data/tournaments/tournaments.json"):
                    json_tournaments_file = model.Model().json_file_playback("tournaments.json")
                    json_tournaments_file.update(self.tournament_information_to_be_created)
                    model.Model().json_file_creation("tournaments.json", json_tournaments_file)
                else:
                    model.Model().json_file_creation("tournaments.json", self.tournament_information_to_be_created)

    def modification_of_the_list_of_rounds(self):
        """Modification of the list of round of the json tournaments file.

        If the list of rounds is equal to "En attente" then this is the first round.
        In this case, we delete the string and add the elements of each round of the json rounds file.
        If rounds were already present then we add the finished round to the suite.
        """
        matches.Matches().next_round()
        json_tournaments_file = model.Model().json_file_playback("tournaments.json")

        list_of_rounds_of_tournament = []
        for tournament_information_of_the_json_file in json_tournaments_file.values():
            list_of_rounds_of_tournament.append(tournament_information_of_the_json_file["Liste des tours"])
        list_of_the_round_to_be_modified = [list_of_rounds_of_tournament[-1]]
        if list_of_the_round_to_be_modified[-1] == "En attente":
            list_of_the_round_to_be_modified.clear()

        json_rounds_file = matches.Matches().update_of_the_json_rounds_file_at_the_end_of_each_round()
        list_of_keys_in_the_json_rounds_file = []
        for file_key_with_tournament_number_and_rounds in json_rounds_file:
            list_of_keys_in_the_json_rounds_file.append(file_key_with_tournament_number_and_rounds)

        list_of_tournament_numbers = []
        for tournament_number in json_tournaments_file:
            list_of_tournament_numbers.append(tournament_number)

        dictionary_with_the_list_of_modified_tournaments = {}
        for each_tournament_number_and_rounds, file_key_with_tournament_number_and_rounds in \
                zip(list_of_keys_in_the_json_rounds_file, json_rounds_file):
            if list_of_tournament_numbers[-1] in each_tournament_number_and_rounds:
                dictionary_with_the_list_of_modified_tournaments.update({
                    file_key_with_tournament_number_and_rounds:
                        json_rounds_file[each_tournament_number_and_rounds]
                })

        self.modification_of_players_scores_in_the_tournament(json_tournaments_file)

        json_tournaments_file[list_of_tournament_numbers[-1]]["Liste des tours"] = \
            dictionary_with_the_list_of_modified_tournaments
        model.Model().json_file_creation("tournaments.json", json_tournaments_file)
        matches.Matches().update_of_the_scores_of_the_json_players_file()

    def modification_of_players_scores_in_the_tournament(self, tournaments_file):
        """Modification of the score of each player of the tournament as and when the matches."""
        json_matches_file = model.Model().json_file_playback("matches.json")
        json_players_file = model.Model().json_file_playback("players.json")

        list_of_round_numbers = []
        for round_number in json_matches_file:
            list_of_round_numbers.append(round_number)

        list_of_tournament_numbers = []
        for tournament_number in tournaments_file:
            list_of_tournament_numbers.append(tournament_number)

        list_of_numbers_of_all_players_in_json_players_file = []
        for player_number in json_players_file:
            list_of_numbers_of_all_players_in_json_players_file.append(player_number)

        for each_match_with_the_player_s_number_and_score, player_information_key in \
                zip(json_matches_file[list_of_round_numbers[-1]].values(),
                    json_players_file[list_of_numbers_of_all_players_in_json_players_file[-2]]):
            json_players_file[list_of_numbers_of_all_players_in_json_players_file[-2]][player_information_key] = \
                each_match_with_the_player_s_number_and_score
            for player_number_and_name in tournaments_file[list_of_tournament_numbers[-1]]["Liste des joueurs"]:
                for player_number_only in each_match_with_the_player_s_number_and_score:
                    if player_number_only in player_number_and_name:
                        tournaments_file[list_of_tournament_numbers[-1]]["Liste des joueurs"][player_number_and_name] \
                            += each_match_with_the_player_s_number_and_score[player_number_only]
