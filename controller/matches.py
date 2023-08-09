import os
import datetime
import re
import sys

sys.path.append("..")
from controller import players
from model import model
from view import manually_retrieve_information

NUMBER_OF_ROUNDS = 4


class Matches:
    def __init__(self):
        self.list_of_winning_players_of_the_round = []
        self.list_of_tied_players_of_the_round = []

    def creation_of_match(self, match_number=0, score=0, round_number=1):
        """Creation of the list of matches with the round and match number, the number of players competing and the
        score of each.
        """
        matches_list = players.Players().random_player_selection()
        current_list_of_matches = {}
        for player_of_each_match in matches_list:
            match_number += 1
            current_list_of_matches.update({
                    f"Match {match_number}": {
                        player_of_each_match[0]: score,
                        player_of_each_match[1]: score
                        }
            })

        if os.path.isfile("../data/tournaments/matches.json"):
            json_matches_file = model.Model().json_file_playback("matches.json")
            for each_round in json_matches_file:
                round_number = int(each_round[-1])
            round_number += 1
            # allows to set the file to 0 when starting a new tournament
            if round_number > NUMBER_OF_ROUNDS:
                os.remove("../data/tournaments/matches.json")
                round_number = 1

        dictionary_of_matches_with_the_current_round = {
            f"Round {round_number}": current_list_of_matches,
        }

        if not os.path.isfile("../data/tournaments/matches.json"):
            model.Model().json_file_creation("matches.json", dictionary_of_matches_with_the_current_round)
        else:
            json_matches_file = model.Model().json_file_playback("matches.json")
            for current_round_number, current_matches in dictionary_of_matches_with_the_current_round.items():
                json_matches_file.update({
                    current_round_number: current_matches,
                })
            model.Model().json_file_creation("matches.json", json_matches_file)

    def creation_of_round(self):
        """Creation of each round with the tournament and the corresponding round number, the list of matches with the
        score of each player, the beginning and end of the date and time of the round. These are generated
        automatically at the time of entry.
        """
        current_list_of_rounds = {}
        json_matches_file = model.Model().json_file_playback("matches.json")
        if os.path.isfile("../data/tournaments/rounds.json"):
            json_rounds_file = model.Model().json_file_playback("rounds.json")
            current_list_of_rounds.update(json_rounds_file)

        current_start_date_and_hour = datetime.datetime.now()
        tour_start_date = current_start_date_and_hour.strftime("%d/%m/%Y")
        tour_start_time = current_start_date_and_hour.strftime("%H:%M:%S")

        rounds_list = []
        for round_number in json_matches_file:
            rounds_list.append(round_number)

        json_tournaments_file = model.Model().json_file_playback("tournaments.json")
        list_of_tournament_numbers = []
        for tournament_number in json_tournaments_file:
            list_of_tournament_numbers.append(tournament_number)
        for matches_of_each_round in json_matches_file.values():
            current_list_of_rounds.update({
                f"{list_of_tournament_numbers[-1]} / {rounds_list[-1]}": matches_of_each_round,
                f"Infos du {list_of_tournament_numbers[-1]} / {rounds_list[-1]}": {
                    "Date de debut": tour_start_date,
                    "Heure de debut": tour_start_time,
                    "Date de fin": "En cours",
                    "Heure de fin": "En cours",
                }
            })
        model.Model().json_file_creation("rounds.json", current_list_of_rounds)

    def end_of_round_result(self):
        """Recovery of winning player and tied player numbers for each round."""
        self.list_of_winning_players_of_the_round.clear()
        self.list_of_tied_players_of_the_round.clear()

        json_matches_file = model.Model().json_file_playback("matches.json")
        list_of_player_numbers = []
        list_of_rounds = []
        ongoing_matches = []
        for each_round in json_matches_file:
            list_of_rounds.append(each_round)
        for player_numbers_and_their_score in json_matches_file[list_of_rounds[-1]].values():
            for player_number in player_numbers_and_their_score:
                retrieving_the_number_only = re.findall(r"[0-9]+", player_number)
                list_of_player_numbers.extend(retrieving_the_number_only)
        for player in range(0, len(list_of_player_numbers), 2):
            ongoing_matches.append(list_of_player_numbers[player:player + 2])
        for each_match in ongoing_matches:
            first_player = each_match[0]
            second_player = each_match[1]
            ask_match_result = \
                manually_retrieve_information.ManuallyRetrieveInformation().know_who_won_at_the_end_of_the_round(
                    first_player, second_player)
            if ask_match_result == "o":
                ask_for_the_winning_player_s_number = \
                    manually_retrieve_information.ManuallyRetrieveInformation().know_the_winning_player_s_number()
                self.list_of_winning_players_of_the_round.append(ask_for_the_winning_player_s_number)
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
            tournament_information["Numero du tour actuel"] += 1
            if tournament_information["Numero du tour actuel"] > NUMBER_OF_ROUNDS:
                tournament_information["Numero du tour actuel"] = NUMBER_OF_ROUNDS
        model.Model().json_file_creation("tournaments.json", json_tournaments_file)

    def recovery_of_the_list_of_rounds(self):
        """Recovery of the list of each round of the current tournament."""
        json_matches_file = model.Model().json_file_playback("matches.json")
        list_of_rounds = []
        for each_round in json_matches_file:
            list_of_rounds.append(each_round)
        return list_of_rounds

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
        """
        json_matches_file = model.Model().json_file_playback("matches.json")
        recovery_of_the_list_of_winning_players_and_tied_players = self.end_of_round_result()
        list_of_winning_players = recovery_of_the_list_of_winning_players_and_tied_players[0]
        list_of_tied_players = recovery_of_the_list_of_winning_players_and_tied_players[1]

        list_of_rounds = self.recovery_of_the_list_of_rounds()
        for player_numbers_and_their_score in json_matches_file[list_of_rounds[-1]].values():
            for player_number in player_numbers_and_their_score:
                for tied_player in list_of_tied_players:
                    if player_number == f"Joueur numero {tied_player}":
                        player_numbers_and_their_score[player_number] += 0.5
                for winning_player in list_of_winning_players:
                    if player_number == f"Joueur numero {winning_player}":
                        player_numbers_and_their_score[player_number] += 1

        model.Model().json_file_creation("matches.json", json_matches_file)
        return json_matches_file

    def update_of_the_json_rounds_file_at_the_end_of_each_round(self):
        """We update the score of the players thanks to the json matches file.
        We add the end date and time of the round retrieved using the recovery_of_the_end_date_and_time_of_the_round
        method.
        """
        json_rounds_file = model.Model().json_file_playback("rounds.json")
        list_of_keys_in_the_json_rounds_file = []
        for file_key_with_tournament_number_and_rounds in json_rounds_file:
            list_of_keys_in_the_json_rounds_file.append(file_key_with_tournament_number_and_rounds)
        json_rounds_file[list_of_keys_in_the_json_rounds_file[-1]]["Date de fin"] = \
            self.recovery_of_the_end_date_and_time_of_the_round()[0]
        json_rounds_file[list_of_keys_in_the_json_rounds_file[-1]]["Heure de fin"] = \
            self.recovery_of_the_end_date_and_time_of_the_round()[1]

        list_of_players_before_match_selection = []
        list_of_players_after_match_selection = []
        for player_numbers_and_their_score in json_rounds_file[list_of_keys_in_the_json_rounds_file[0]].values():
            for player_number in player_numbers_and_their_score:
                list_of_players_before_match_selection.append(player_number)
        for player in range(0, len(list_of_players_before_match_selection), 2):
            list_of_players_after_match_selection.append(list_of_players_before_match_selection[player:player + 2])

        list_of_all_match_numbers = []
        for matches_and_their_information in json_rounds_file.values():
            for keys_corresponding_to_match_numbers_and_start_and_end_dates_and_times in matches_and_their_information:
                match_number = re.findall(r"Match [0-9]+",
                                          keys_corresponding_to_match_numbers_and_start_and_end_dates_and_times)
                list_of_all_match_numbers.extend(match_number)

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

        matches_list = []
        for first_round_matches in json_rounds_file.values():
            matches_list.extend(first_round_matches)
            break

        list_of_keys_in_the_json_rounds_file = []
        for file_key_with_tournament_number_and_rounds in json_rounds_file:
            list_of_keys_in_the_json_rounds_file.append(file_key_with_tournament_number_and_rounds)

        for number in range(0, len(matches_list)):
            match_with_players_number_and_score = \
                json_rounds_file[list_of_keys_in_the_json_rounds_file[-2]][matches_list[number]]
            for player_number, player_score in match_with_players_number_and_score.items():
                final_score_of_players_at_the_end_of_the_game.update({player_number: player_score})

        for player_number, information_about_player in json_players_file.items():
            if player_number in final_score_of_players_at_the_end_of_the_game:
                information_about_player["Score"] += final_score_of_players_at_the_end_of_the_game[player_number]

        model.Model().json_file_creation("players.json", json_players_file)
