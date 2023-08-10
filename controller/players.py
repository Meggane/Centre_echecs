import re
import os
import random
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
                    in zip(manually_retrieve_information.ManuallyRetrieveInformation().player_s_family_name(),
                           manually_retrieve_information.ManuallyRetrieveInformation().player_s_first_name(),
                           manually_retrieve_information.ManuallyRetrieveInformation().player_s_date_of_birth()):
                dictionary_of_all_players.update({
                    f"Joueur numero {player_number}": {
                        "Nom de famille": each_family_name,
                        "Prenom": each_first_name,
                        "Date de naissance": each_date_of_birth,
                        "Score": score
                    },
                })
                add_new_player = manually_retrieve_information.ManuallyRetrieveInformation().adding_a_new_player()
        model.Model().json_file_creation("players.json", dictionary_of_all_players)

    def randomly_mix_players(self):
        """Randomly mix players to create random matches for the first game."""
        json_tournaments_file = model.Model().json_file_playback("tournaments.json")
        list_of_player_numbers = []
        for tournament_information in json_tournaments_file.values():
            number_of_each_player = re.findall(r"Joueur numero [0-9]+",
                                               str(tournament_information["Liste des joueurs"]))
            list_of_player_numbers.append(number_of_each_player)
        mix_of_players = random.sample(list_of_player_numbers[-1], len(list_of_player_numbers[-1]))
        return mix_of_players

    def random_player_selection(self):
        """Define players who play together according to the random list of players."""
        mixed_list_players = self.randomly_mix_players()
        matches_list = []
        for two_in_two_index in range(0, len(mixed_list_players), 2):
            matches_list.append(mixed_list_players[two_in_two_index:two_in_two_index + 2])
        return matches_list

    def player_ranking(self):
        """Rank players according to their score.

        We get the score of each player according to the selected json file then we classify them.
        """
        scores = {}
        json_tournaments_file = model.Model().json_file_playback("tournaments.json")
        liste_num_tournoi = []
        for num_tournoi in json_tournaments_file:
            liste_num_tournoi.append(num_tournoi)

        for player_num_and_name, player_score in \
                json_tournaments_file[liste_num_tournoi[-1]]["Liste des joueurs"].items():
            player_num = re.findall(r"Joueur numero [0-9]+", player_num_and_name)
            scores.update({"".join(player_num): player_score})
        ranking_of_players = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return ranking_of_players
