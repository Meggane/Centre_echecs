import re
import os
import random
import time
import sys

sys.path.append("..")
from model import model
from view import manually_retrieve_information


class Players:
    def __init__(self):
        self.scores = {}

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
                    f"Joueur numéro {player_number}": {
                        "Nom de famille": each_family_name,
                        "Prénom": each_first_name,
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
            number_of_each_player = re.findall(r"Joueur numéro [0-9]+",
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
        self.scores = {}
        json_tournaments_file = model.Model().json_file_playback("tournaments.json")
        liste_num_tournoi = []
        for num_tournoi in json_tournaments_file:
            liste_num_tournoi.append(num_tournoi)

        for player_num_and_name, player_score in \
                json_tournaments_file[liste_num_tournoi[-1]]["Liste des joueurs"].items():
            player_num = re.findall(r"Joueur numéro [0-9]+", player_num_and_name)
            self.scores.update({"".join(player_num): player_score})
        ranking_of_players = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        return ranking_of_players

    def definition_of_the_rank_of_the_players(self):
        """Assign the rank of the player according to his ranking.

        If several players have the same score then they have the same rank and we skip the necessary number of ranks
        for the next.
        """
        player_ranking_list = self.player_ranking()
        score_list = []
        player_list = []
        for player in player_ranking_list:
            score_list.append(player[1])
            player_list.append(player[0])

        player_score_without_duplicate = sorted(set(score_list), reverse=True)
        list_of_rank = []
        number_of_different_scores = len(player_score_without_duplicate)
        for list_score_index in range(0, number_of_different_scores):
            for player in player_ranking_list:
                if player[1] == player_score_without_duplicate[list_score_index]:
                    if len(list_of_rank) > 1 and list_of_rank[-1] != list_of_rank[-2]:
                        current_rank = len(list_of_rank) + 1
                    else:
                        current_rank = list_score_index + 1
                        if len(list_of_rank) > 1 and current_rank != list_of_rank[-1]:
                            current_rank = len(list_of_rank) + 1
                    list_of_rank.append(current_rank)

        dictionary_with_the_rank_of_each_player = {}
        for player_number, rank in zip(player_list, list_of_rank):
            dictionary_with_the_rank_of_each_player.update({
                f"{player_number}": f"Rang {rank}"
            })
        return dictionary_with_the_rank_of_each_player

    def matches_selection_based_on_player_ranking(self):
        """Selection of matches according to the ranking of each player.

        If two players have the same rank then we draw lots to determine who will play against whom.
        """
        ranking = self.definition_of_the_rank_of_the_players()
        rank_of_players = []
        for rank_of_each_player in ranking.values():
            rank_of_players.append(rank_of_each_player)

        # recovers all the ranks of all players if some have the same.
        rank_list = sorted(set(rank_of_players))
        number_of_players_ranked_according_to_their_rank = []
        for each_rank in rank_list:
            several_lists_with_in_each_the_list_of_players_with_the_same_rank = \
                [player_number for player_number, player_rank in ranking.items()
                 if player_rank == each_rank]

            mix_of_players_with_the_same_rank = \
                random.sample(several_lists_with_in_each_the_list_of_players_with_the_same_rank,
                              len(several_lists_with_in_each_the_list_of_players_with_the_same_rank))
            number_of_players_ranked_according_to_their_rank.extend([each_player for each_player
                                                                     in mix_of_players_with_the_same_rank])
        return number_of_players_ranked_according_to_their_rank

    def selection_of_players_who_will_play_together_according_to_their_ranking(self):
        """Selection of players to play together."""
        matches_list = []
        number_of_players_ranked_according_to_their_rank = self.matches_selection_based_on_player_ranking()
        for each_player in range(0, len(number_of_players_ranked_according_to_their_rank), 2):
            matches_list.append(number_of_players_ranked_according_to_their_rank
                                [each_player:each_player + 2])
        return matches_list

    def recovery_of_players_who_have_already_played_together(self):
        """Recovering of the list of players who have already played against each other."""
        json_matches_file = model.Model().json_file_playback("matches.json")
        player_numbers_who_have_already_played_together = []
        for round_match_dictionary in json_matches_file.values():
            for players_who_played_together in round_match_dictionary.values():
                player_numbers_who_have_already_played_together.append(list(players_who_played_together))
        return player_numbers_who_have_already_played_together

    def modification_of_the_match_list(self, list_with_player_ranking, list_with_modified_player_ranking):
        """We change the list of matches according to the ranking of players"""
        for each_player in range(0, len(list_with_player_ranking), 2):
            list_with_modified_player_ranking.append(list_with_player_ranking[each_player:each_player + 2])
        return list_with_modified_player_ranking

    def change_the_order_of_players_in_the_match_list(self, list_with_player_ranking,
                                                      index_of_the_player_to_be_deleted,
                                                      index_where_to_place_the_player):
        """We change the list of matches if the players have already played together while respecting the ranking"""
        deletion_of_the_player = list_with_player_ranking.pop(index_of_the_player_to_be_deleted)
        list_with_player_ranking.insert(index_where_to_place_the_player, deletion_of_the_player)
        return list_with_player_ranking

    def change_of_players_playing_together(self):
        """New list of players who will play together after retrieving the list of players who have already played
        against each other.
        """
        players_who_have_already_played_against = self.recovery_of_players_who_have_already_played_together()
        list_with_player_ranking = self.matches_selection_based_on_player_ranking()
        list_with_modified_player_ranking = []
        number_and_index_of_players = {}
        for each_pair_of_players in players_who_have_already_played_against:
            for each_player in each_pair_of_players:
                index_of_player = list_with_player_ranking.index("".join(each_player))
                number_and_index_of_players.update({
                    each_player: index_of_player
                })

        # We create a new list of matches with players who have never played against each other
        self.modification_of_the_match_list(list_with_player_ranking, list_with_modified_player_ranking)

        # We define a time for the execution of the while loop
        start_time = time.time()
        max_execution_time = 2

        index_being = 0
        while index_being < len(players_who_have_already_played_against):
            two_players_have_already_played_together = False
            for players_of_the_match in list_with_modified_player_ranking:
                two_players_have_already_played_together = False
                if players_of_the_match == players_who_have_already_played_against[index_being] or \
                        players_of_the_match[::-1] == players_who_have_already_played_against[index_being]:
                    index_of_the_player_to_be_deleted = number_and_index_of_players[players_of_the_match[1]]
                    index_where_to_place_the_player = index_of_the_player_to_be_deleted + 1
                    self.change_the_order_of_players_in_the_match_list(list_with_player_ranking,
                                                                       index_of_the_player_to_be_deleted,
                                                                       index_where_to_place_the_player)
                    list_with_modified_player_ranking.clear()
                    self.modification_of_the_match_list(list_with_player_ranking, list_with_modified_player_ranking)
                    # Reset the index to restart the loop
                    index_being = 0
                    two_players_have_already_played_together = True
                    if time.time() - start_time > max_execution_time:
                        number_of_players_in_the_tournament = len(list_with_player_ranking)
                        random_index = random.randint(1, number_of_players_in_the_tournament - 2)
                        random_index_between_two_players = random.randint(0, 1)
                        index_of_the_player_of_the_match_to_be_deleted = \
                            number_and_index_of_players[players_of_the_match[random_index_between_two_players]]
                        index_where_to_place_the_player = index_of_the_player_of_the_match_to_be_deleted - random_index
                        self.change_the_order_of_players_in_the_match_list(list_with_player_ranking,
                                                                           index_of_the_player_to_be_deleted,
                                                                           index_where_to_place_the_player)
                        continue
                    break
            if two_players_have_already_played_together == False:
                index_being += 1
        return list_with_modified_player_ranking

    def color_of_the_pieces_of_the_chessboard(self):
        """Randomly select which player of the match plays white and which one plays black"""
        random_drawing = random.randint(0, 1)
        if random_drawing == 0:
            color_of_the_first_player_s_pieces = "Noir"
            color_of_the_second_player_s_pieces = "Blanc"
        else:
            color_of_the_first_player_s_pieces = "Blanc"
            color_of_the_second_player_s_pieces = "Noir"
        return color_of_the_first_player_s_pieces, color_of_the_second_player_s_pieces

    def sort_players_alphabetically(self):
        """Recovery of the list of each player’s family names and sort them alphabetically."""
        players_list = model.Model().json_file_playback("players.json")
        list_of_players = []
        for player_information in players_list.values():
            list_of_players.append(f"{player_information['Nom de famille']} {player_information['Prénom']}")
        sorting_of_players = sorted(list_of_players)
        return sorting_of_players
