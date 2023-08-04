import os
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
