import os
import datetime
import sys

sys.path.append("..")
from controller import players
from model import model

NUMBER_OF_ROUNDS = 4


class Matches:
    def __init__(self):
        pass

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
