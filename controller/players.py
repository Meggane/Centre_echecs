import re
import os
import sys

sys.path.append("..")
from model import model
from view import manually_retrieve_information


class Players:
    def __init__(self):
        pass

    def add_players(self, add_new_player="o", player_number=0, score=0):
        """Add players to the tournament with the control terminal.

        Recovery of the entry family_name, first_name and date_of_birth.

        The number of each player is added automatically.
        """
        dictionary_of_all_players = {}
        if os.path.isfile("../data/tournaments/players.json"):
            recovery_of_the_json_file_with_list_of_players = model.Model().json_file_playback("players.json")
            dictionary_of_all_players.update(recovery_of_the_json_file_with_list_of_players)
            for each_player in recovery_of_the_json_file_with_list_of_players:
                recovery_of_the_number_of_each_player = re.findall(r"[0-9]+", each_player)
                list_of_all_numbers = list(map(int, recovery_of_the_number_of_each_player))
                player_number = list_of_all_numbers[-1]

        while add_new_player == "o":
            player_number += 1
            for each_family_name, each_first_name, each_date_of_birth \
                    in zip(manually_retrive_information.ManuallyRetrieveInformation().player_s_family_name(),
                           manually_retrive_information.ManuallyRetrieveInformation().player_s_first_name(),
                           manually_retrive_information.ManuallyRetrieveInformation().player_s_date_of_birth()):
                dictionary_of_all_players.update({
                    f"Joueur numero {player_number}": {
                        "Nom de famille": each_family_name,
                        "Prenom": each_first_name,
                        "Date de naissance": each_date_of_birth,
                        "Score": score
                    },
                })
                add_new_player = manually_retrive_information.ManuallyRetrieveInformation().adding_a_new_player()
        model.Model().json_file_creation("players.json", dictionary_of_all_players)
