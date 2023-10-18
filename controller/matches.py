import os
import datetime
import re
import sys

sys.path.append("..")
from controller import players
from model import model
from view import manually_retrieve_information
from controller import InformationRetrieval
from view import tournament_information as python_tournament_information_file


class Matches:
    def __init__(self):
        self.list_of_winning_players_of_the_round = []
        self.list_of_tied_players_of_the_round = []

    def creation_of_the_match_list(self, match_number=0, score=0, round_number=1):
        """Creation of the list of matches with the round and match number, the number of players competing and the
        score of each.
        """
        matches_list = []
        try:
            json_matches_file = model.Model().json_file_playback("matches.json")
            for each_round in json_matches_file:
                round_number = int(each_round[-1])
            round_number += 1
            # allows to set the file to 0 when starting a new tournament
            if round_number > python_tournament_information_file.NUMBER_OF_ROUNDS:
                os.remove("data/tournaments/matches.json")
                round_number = 1
                matches_list.extend(players.Players().random_player_selection())
            else:
                matches_list.extend(players.Players().change_of_players_playing_together())
        except FileNotFoundError:
            matches_list.extend(players.Players().random_player_selection())

        current_list_of_matches = {}
        for player_of_each_match in matches_list:
            match_number += 1
            current_list_of_matches.update({
                f"Match {match_number}": {
                    player_of_each_match[0]: score,
                    player_of_each_match[1]: score
                }
            })
        dictionary_of_matches_with_the_current_round = {
            f"Round {round_number}": current_list_of_matches,
        }
        return dictionary_of_matches_with_the_current_round

    def creation_of_match(self):
        """Creation of the matches.json file"""
        recovery_of_the_match_list = self.creation_of_the_match_list()
        try:
            json_matches_file = model.Model().json_file_playback("matches.json")
            for current_round_number, current_matches in recovery_of_the_match_list.items():
                json_matches_file.update({
                    current_round_number: current_matches,
                })
            model.Model().json_file_creation("matches.json", json_matches_file)
        except FileNotFoundError:
            model.Model().json_file_creation("matches.json", recovery_of_the_match_list)

    def creation_of_round(self):
        """Creation of each round with the tournament and the corresponding round number, the list of matches with the
        score of each player, the beginning and end of the date and time of the round. And finally, the color with
        which the players play the match. These are generated automatically at the time of entry.
        """
        try:
            json_tournaments_file = model.Model().json_file_playback("tournaments.json")
            self.creation_of_match()
            current_list_of_rounds = {}
            json_matches_file = model.Model().json_file_playback("matches.json")
            try:
                json_rounds_file = model.Model().json_file_playback("rounds.json")
                current_list_of_rounds.update(json_rounds_file)
            except FileNotFoundError:
                pass

            current_start_date_and_hour = datetime.datetime.now()
            tour_start_date = current_start_date_and_hour.strftime("%d/%m/%Y")
            tour_start_time = current_start_date_and_hour.strftime("%H:%M:%S")
            rounds_list = InformationRetrieval().retrieval_of_dictionary_keys(json_matches_file)
            list_of_tournament_numbers = InformationRetrieval().retrieval_of_dictionary_keys(json_tournaments_file)
            for matches_of_each_round in json_matches_file.values():
                color_used_for_each_player = {}
                for each_match in matches_of_each_round.values():
                    players_of_each_match = []
                    players_of_each_match.extend(each_match.keys())
                    color_randomly_assigned_to_each_player = InformationRetrieval().retrieval_of_dictionary_keys(
                        players.Players().color_of_the_pieces_of_the_chessboard())
                    color_used_for_each_player.update({
                            "".join(players_of_each_match[0]): color_randomly_assigned_to_each_player[0],
                            "".join(players_of_each_match[1]): color_randomly_assigned_to_each_player[1]
                        })
                current_list_of_rounds.update({
                    f"{list_of_tournament_numbers[-1]} / {rounds_list[-1]}": matches_of_each_round,
                    f"Infos du {list_of_tournament_numbers[-1]} / {rounds_list[-1]}": {
                        "Date de début": tour_start_date,
                        "Heure de début": tour_start_time,
                        "Date de fin": "En cours",
                        "Heure de fin": "En cours",
                        "Couleur des pièces des joueurs des matchs": color_used_for_each_player
                    }
                })
            model.Model().json_file_creation("rounds.json", current_list_of_rounds)
        except FileNotFoundError:
            print("Vous ne pouvez pas débuter de match tant que vous n'avez pas créé un tournoi")

    def end_of_round_result(self):
        """Recovery of winning player and tied player numbers for each round."""
        self.list_of_winning_players_of_the_round.clear()
        self.list_of_tied_players_of_the_round.clear()
        json_matches_file = model.Model().json_file_playback("matches.json")
        list_of_player_numbers = []
        list_of_rounds = InformationRetrieval().retrieval_of_dictionary_keys(json_matches_file)
        for player_numbers_and_their_score in json_matches_file[list_of_rounds[-1]].values():
            for player_number in player_numbers_and_their_score:
                retrieving_the_number_only = re.findall(r"[0-9]+", player_number)
                list_of_player_numbers.extend(retrieving_the_number_only)
        ongoing_matches = InformationRetrieval().recovery_of_players_by_two(list_of_player_numbers)
        for each_match in ongoing_matches:
            first_player = each_match[0]
            second_player = each_match[1]
            ask_match_result = \
                manually_retrieve_information.ManuallyRetrieveInformation().know_who_won_at_the_end_of_the_round(
                    first_player, second_player)
            if ask_match_result == "o":
                player_numbers_match = False
                while player_numbers_match is False:
                    ask_for_the_winning_player_s_number = \
                        manually_retrieve_information.ManuallyRetrieveInformation().know_the_winning_player_s_number()
                    if first_player == ask_for_the_winning_player_s_number or second_player == \
                            ask_for_the_winning_player_s_number:
                        self.list_of_winning_players_of_the_round.append(ask_for_the_winning_player_s_number)
                        player_numbers_match = True
                    else:
                        print("Erreur dans le numéro de joueur.")
            else:
                self.list_of_tied_players_of_the_round.append(first_player)
                self.list_of_tied_players_of_the_round.append(second_player)
        return self.list_of_winning_players_of_the_round, self.list_of_tied_players_of_the_round

    def next_round(self):
        """Modification of the current tournament round.

        If the number of rounds is greater than NUMBER_OF_ROUNDS then the tournament is over.
        """
        json_tournaments_file = model.Model().json_file_playback("tournaments.json")
        for tournament_information in json_tournaments_file.values():
            tournament_information["Numéro du tour actuel"] += 1
            if tournament_information["Numéro du tour actuel"] > python_tournament_information_file.NUMBER_OF_ROUNDS:
                tournament_information["Numéro du tour actuel"] = python_tournament_information_file.NUMBER_OF_ROUNDS
        model.Model().json_file_creation("tournaments.json", json_tournaments_file)

    def recovery_of_the_end_date_and_time_of_the_round(self):
        """Recovery of the date and time of the end of the current round.

        This is done automatically at the time of the end of the round entry.
        """
        current_end_date_and_time = datetime.datetime.now()
        round_end_date = current_end_date_and_time.strftime("%d/%m/%Y")
        round_end_time = current_end_date_and_time.strftime("%H:%M:%S")
        return round_end_date, round_end_time

    def update_of_the_score_of_the_json_matches_file(self):
        """Number of points earned by players at the end of the match.

        The winning player wins 1 point.
        The losing player wins 0 point.
        In the event of a tie, each player wins 0.5 point.

        We return the new matches json file with the new match results.
        """
        json_matches_file = model.Model().json_file_playback("matches.json")
        recovery_of_the_list_of_winning_players_and_tied_players = self.end_of_round_result()
        list_of_winning_players = recovery_of_the_list_of_winning_players_and_tied_players[0]
        list_of_tied_players = recovery_of_the_list_of_winning_players_and_tied_players[1]
        list_of_rounds = InformationRetrieval().retrieval_of_dictionary_keys(json_matches_file)
        for player_numbers_and_their_score in json_matches_file[list_of_rounds[-1]].values():
            for player_number in player_numbers_and_their_score:
                for tied_player in list_of_tied_players:
                    if player_number == f"Joueur numéro {tied_player}":
                        player_numbers_and_their_score[player_number] += 0.5
                for winning_player in list_of_winning_players:
                    if player_number == f"Joueur numéro {winning_player}":
                        player_numbers_and_their_score[player_number] += 1
        model.Model().json_file_creation("matches.json", json_matches_file)
        return json_matches_file

    def update_of_the_json_rounds_file_at_the_end_of_each_round(self):
        """We update the score of the players thanks to the json matches file.
        We add the end date and time of the round retrieved using the recovery_of_the_end_date_and_time_of_the_round
        method.

        We return the new rounds json file with the new match results and the end date and time of the round.
        """
        json_rounds_file = model.Model().json_file_playback("rounds.json")
        list_of_keys_in_the_json_rounds_file = InformationRetrieval().retrieval_of_dictionary_keys(json_rounds_file)
        json_rounds_file[list_of_keys_in_the_json_rounds_file[-1]]["Date de fin"] = \
            self.recovery_of_the_end_date_and_time_of_the_round()[0]
        json_rounds_file[list_of_keys_in_the_json_rounds_file[-1]]["Heure de fin"] = \
            self.recovery_of_the_end_date_and_time_of_the_round()[1]
        json_matches_file = self.update_of_the_score_of_the_json_matches_file()
        for all_matches_with_players_and_scores in json_matches_file.values():
            for player_numbers_and_their_score, match_number_to_be_changed in \
                    zip(all_matches_with_players_and_scores.values(),
                        json_rounds_file[list_of_keys_in_the_json_rounds_file[-2]]):
                json_rounds_file[list_of_keys_in_the_json_rounds_file[-2]][match_number_to_be_changed] = \
                    player_numbers_and_their_score
        model.Model().json_file_creation("rounds.json", json_rounds_file)
        return json_rounds_file

    def update_of_the_scores_of_the_json_players_file(self):
        """Update the scores of each player at the end of each match in the players.json file."""
        final_score_of_players_at_the_end_of_the_game = {}
        json_players_file = model.Model().json_file_playback("players.json")
        json_rounds_file = model.Model().json_file_playback("rounds.json")
        liste_des_keys_rounds = InformationRetrieval().retrieval_of_dictionary_keys(json_rounds_file)
        matches_list = InformationRetrieval().retrieval_of_dictionary_keys(json_rounds_file[liste_des_keys_rounds[-2]])
        list_of_keys_in_the_json_rounds_file = InformationRetrieval().retrieval_of_dictionary_keys(json_rounds_file)
        for number in range(0, len(matches_list)):
            match_with_players_number_and_score = \
                json_rounds_file[list_of_keys_in_the_json_rounds_file[-2]][matches_list[number]]
            for player_number, player_score in match_with_players_number_and_score.items():
                final_score_of_players_at_the_end_of_the_game.update({player_number: player_score})
        for player_number, information_about_player in json_players_file.items():
            if player_number in final_score_of_players_at_the_end_of_the_game:
                information_about_player["Score"] += final_score_of_players_at_the_end_of_the_game[player_number]
        model.Model().json_file_creation("players.json", json_players_file)
