import re
import sys

sys.path.append("..")
from view import tournament_information
from model import model
from controller import matches
from controller import InformationRetrieval


class Tournaments:
    def __init__(self):
        self.tournament_information_to_be_created = {}

    def recovery_of_the_number_of_all_players(self):
        """We get the numbers of all the players from the json players file."""
        json_players_file = model.Model().json_file_playback("players.json")
        list_of_player_number = []
        for player_number in json_players_file:
            list_of_player_number.extend(re.findall(r"[0-9]+", player_number))
        return list_of_player_number

    def recovery_of_the_number_and_name_of_all_players(self):
        """We get the numbers and names of all the players from the json players file.

        The result allows to compare these players with the players added to the tournament in the json tournaments
        file.
        """
        json_players_file = model.Model().json_file_playback("players.json")
        list_of_players_in_json_file = []
        for player_number, player_information in json_players_file.items():
            list_of_players_in_json_file.append(f"{player_number} / {player_information['Nom de famille']} "
                                                f"{player_information['Prénom']}")
        return list_of_players_in_json_file

    def check_if_json_tournaments_file_exists(self, tournament_number=1):
        """We check if the json tournaments file exists.
        If it exists we get the number of the last tournament and increase it by 1 to create a new tournament.
        If it does not exist then the tournament number is 1 because it is the first tournament.
        """
        try:
            json_tournaments_file = model.Model().json_file_playback("tournaments.json")
            list_of_number_of_each_tournament = []
            for number_of_each_tournament in \
                    InformationRetrieval().retrieval_of_dictionary_keys(json_tournaments_file):
                retrieving_the_number_only = re.findall(r"[0-9]+", number_of_each_tournament)
                list_of_number_of_each_tournament.extend(list(map(int, retrieving_the_number_only)))
            number_of_the_last_tournament = list_of_number_of_each_tournament[-1]
            number_of_the_last_tournament += 1
            tournament_number = number_of_the_last_tournament
        except FileNotFoundError:
            pass
        return tournament_number

    def recovery_of_information_to_create_a_tournament(self, score=0):
        """Tournament information.

        Each tournament has a number and the information collected from the user.
        The number of rounds is set by default to 4.
        Only the current round number and the list of rounds will change throughout the tournament.
        """
        tournament_number = self.check_if_json_tournaments_file_exists()
        list_of_tournament_information = InformationRetrieval().retrieval_of_dictionary_keys(
            tournament_information.TournamentInformation().recovery_of_tournament_information())
        number_of_rounds_of_the_tournament = tournament_information.NUMBER_OF_ROUNDS
        list_of_players_to_add = tournament_information.TournamentInformation().selection_of_players_to_add()
        player_number_added_incorrect = False
        all_players_added_to_the_tournament = set()
        list_of_players_of_the_tournament_with_their_score = {}
        try:
            match len(list_of_players_to_add):
                case n if n < 6:
                    print("Vous n'avez pas ajouté suffisamment de participant. Veuillez réessayer.")
                    player_number_added_incorrect = True
                case n if n % 2 != 0:
                    print("Le nombre de participant n'est pas pair. Veuillez réessayer.")
                    player_number_added_incorrect = True
                case _:
                    for player_number_added in list_of_players_to_add:
                        if player_number_added in all_players_added_to_the_tournament:
                            print("Vous avez ajouté un joueur en double. Veuillez réessayer.")
                            player_number_added_incorrect = True
                        elif player_number_added not in self.recovery_of_the_number_of_all_players():
                            print("Un numéro de joueur sélectionné n'existe pas. Veuillez réessayer.")
                            player_number_added_incorrect = True
                        all_players_added_to_the_tournament.add(player_number_added)
                    list_of_numbers_of_players_participating_in_the_tournament = list(map(int, list_of_players_to_add))
                    liste_tournoi_players = []
                    for list_index in range(len(self.recovery_of_the_number_and_name_of_all_players())):
                        for number_of_player_participating_in_the_tournament \
                                in list_of_numbers_of_players_participating_in_the_tournament:
                            if list_index == number_of_player_participating_in_the_tournament - 1:
                                liste_tournoi_players.append(self.recovery_of_the_number_and_name_of_all_players()
                                                             [list_index])
                    for index_of_each_player_in_json_players_file in \
                            range(len(self.recovery_of_the_number_and_name_of_all_players())):
                        for player_number_in_the_tournament in \
                                list_of_numbers_of_players_participating_in_the_tournament:
                            if index_of_each_player_in_json_players_file == player_number_in_the_tournament - 1:
                                list_of_players_of_the_tournament_with_their_score.update({
                                    self.recovery_of_the_number_and_name_of_all_players()[
                                        index_of_each_player_in_json_players_file]: score
                                })
        except ValueError:
            print("Le numéro des joueurs peut être uniquement des chiffres. Veuillez réessayer.")
        return tournament_number, list_of_tournament_information, number_of_rounds_of_the_tournament, \
            list_of_players_of_the_tournament_with_their_score, player_number_added_incorrect

    def creation_of_tournament(self):
        """Tournament creation.

        We retrieve the information entered by the user and create or modify the json tournaments file.
        """
        try:
            model.Model().json_file_playback("players.json")
            recovery_of_tournament_items = self.recovery_of_information_to_create_a_tournament()
            tournament_number = recovery_of_tournament_items[0]
            list_of_tournament_information = recovery_of_tournament_items[1]
            number_of_rounds_of_the_tournament = recovery_of_tournament_items[2]
            list_of_players_of_the_tournament_with_their_score = recovery_of_tournament_items[3]
            player_number_added_incorrect = recovery_of_tournament_items[4]
            self.tournament_information_to_be_created.update({
                f"Tournoi numéro {tournament_number}": {
                    "Nom du tournoi": list_of_tournament_information[0],
                    "Lieu du tournoi": list_of_tournament_information[1],
                    "Date de début du tournoi": list_of_tournament_information[2],
                    "Date de fin du tournoi": list_of_tournament_information[3],
                    "Nombre de tour": number_of_rounds_of_the_tournament,
                    "Numéro du tour actuel": 1,
                    "Liste des tours": "En attente",
                    "Liste des joueurs": list_of_players_of_the_tournament_with_their_score,
                    "Description": list_of_tournament_information[4]
                }
            })
            if player_number_added_incorrect is False:
                try:
                    json_tournaments_file = model.Model().json_file_playback("tournaments.json")
                    json_tournaments_file.update(self.tournament_information_to_be_created)
                    model.Model().json_file_creation("tournaments.json", json_tournaments_file)
                except FileNotFoundError:
                    model.Model().json_file_creation("tournaments.json", self.tournament_information_to_be_created)
                except NameError:
                    model.Model().json_file_creation("tournaments.json", self.tournament_information_to_be_created)
        except FileNotFoundError:
            print("Vous ne pouvez pas créer de tournoi tant que vous n'avez pas de joueurs")

    def modification_of_the_list_of_rounds(self):
        """Modification of the list of round of the json tournaments file.

        If the list of rounds is equal to "En attente" then this is the first round.
        In this case, we delete the string and add the elements of each round of the json rounds file.
        If rounds were already present then we add the finished round to the suite.
        """
        try:
            model.Model().json_file_playback("matches.json")
            matches.Matches().next_round()
            json_tournaments_file = model.Model().json_file_playback("tournaments.json")
            list_of_rounds_of_tournament = []
            for tournament_information_of_the_json_file in \
                    InformationRetrieval().retrieval_of_dictionary_values(json_tournaments_file):
                list_of_rounds_of_tournament.append(tournament_information_of_the_json_file["Liste des tours"])
            list_of_the_round_to_be_modified = [list_of_rounds_of_tournament[-1]]
            if list_of_the_round_to_be_modified[-1] == "En attente":
                list_of_the_round_to_be_modified.clear()
            json_rounds_file = matches.Matches().update_of_the_json_rounds_file_at_the_end_of_each_round()
            list_of_keys_in_the_json_rounds_file = InformationRetrieval().retrieval_of_dictionary_keys(json_rounds_file)
            list_of_tournament_numbers = InformationRetrieval().retrieval_of_dictionary_keys(json_tournaments_file)
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
        except FileNotFoundError:
            print("Vous ne pouvez pas finir un match tant qu'il n'a pas débuté")

    def modification_of_players_scores_in_the_tournament(self, tournaments_file):
        """Modification of the score of each player of the tournament as and when the matches."""
        json_matches_file = model.Model().json_file_playback("matches.json")
        json_players_file = model.Model().json_file_playback("players.json")
        list_of_round_numbers = InformationRetrieval().retrieval_of_dictionary_keys(
            InformationRetrieval().retrieval_of_dictionary_keys(json_matches_file))
        list_of_tournament_numbers = InformationRetrieval().retrieval_of_dictionary_keys(
            InformationRetrieval().retrieval_of_dictionary_keys(tournaments_file))
        list_of_numbers_of_all_players_in_json_players_file = InformationRetrieval().retrieval_of_dictionary_keys(
            InformationRetrieval().retrieval_of_dictionary_keys(json_players_file))
        for each_match_with_the_player_s_number_and_score in json_matches_file[list_of_round_numbers[-1]].values():
            for player_information_key in json_players_file[list_of_numbers_of_all_players_in_json_players_file[-2]]:
                json_players_file[list_of_numbers_of_all_players_in_json_players_file[-2]][player_information_key] = \
                    each_match_with_the_player_s_number_and_score
            for player_number_and_name in tournaments_file[list_of_tournament_numbers[-1]]["Liste des joueurs"]:
                for player_number_only in each_match_with_the_player_s_number_and_score:
                    if player_number_only in player_number_and_name:
                        # We check that the exact numbers of the players match to avoid that the numbers of the players
                        # as for example the 10 adds twice the score of the player number 1.
                        player_number_retrieval = re.findall(r"Joueur numéro [0-9]+", player_number_and_name)
                        number_of_the_player_to_check = "".join(player_number_retrieval)
                        if player_number_only == number_of_the_player_to_check:
                            tournaments_file[list_of_tournament_numbers[-1]]["Liste des joueurs"][
                                player_number_and_name] += each_match_with_the_player_s_number_and_score[
                                player_number_only]
