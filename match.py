import re
import random
import os
import players
import turns


list_of_winning_players = []
list_of_tied_players = []


class Match:
    def __int__(self):
        self.player_score = []

    def creation_of_the_json_file_with_match_list(self):
        """Creation of matches.json file to get the list of matches according to the rounds and the players list for
        each match.

        Afterwards, this file allows to know which players have already played together.
        """
        list_of_matches = players.Players().random_player_selection()
        match_number = 1
        dictionary_with_list_of_matches_and_players = {}
        for each_match in list_of_matches:
            dictionary_with_list_of_matches_and_players.update({
                f"Match {match_number}": f"{each_match[0]} contre {each_match[1]}",
            })
            match_number += 1

        recovery_of_the_dictionary_with_list_of_matches_and_players = {}
        round_number = 1
        for dictionary_key, dictionary_value in dictionary_with_list_of_matches_and_players.items():
            recovery_of_the_dictionary_with_list_of_matches_and_players.update({dictionary_key: dictionary_value})

        dictionary_with_list_of_matches_and_players.clear()

        if os.path.isfile("matches.json"):
            recovery_of_the_json_file_with_list_of_matches_and_players = \
                players.Players().json_file_playback("matches.json")
            for each_round in recovery_of_the_json_file_with_list_of_matches_and_players:
                round_number = int(each_round[-1])
            round_number += 1
        dictionary_with_list_of_matches_and_players.update({
            f"Tour {round_number}": recovery_of_the_dictionary_with_list_of_matches_and_players,
        })

        if not os.path.isfile("matches.json"):
            players.Players().json_file_creation("matches.json", dictionary_with_list_of_matches_and_players)
        else:
            recovery_of_the_json_file_with_list_of_matches_and_players = \
                players.Players().json_file_playback("matches.json")
            for dictionary_key, dictionary_value in dictionary_with_list_of_matches_and_players.items():
                recovery_of_the_json_file_with_list_of_matches_and_players.update({
                    dictionary_key: dictionary_value,
                })
            players.Players().json_file_creation("matches.json",
                                                 recovery_of_the_json_file_with_list_of_matches_and_players)

    def end_of_game_result(self):
        """Recovery of winning player and tied player numbers."""
        ongoing_matches = players.Players().random_player_selection()
        for each_match in ongoing_matches:
            players_in_the_match = "".join(each_match)
            number_of_players_in_the_match = re.findall(r"[0-9]", players_in_the_match)
            ask_match_result = input(" contre ".join(each_match) + " | Y a t-il un gagnant ? (o/n)")
            if ask_match_result == "o":
                ask_for_the_winning_player_s_number = input("Numéro du joueur gagnant : ")
                list_of_winning_players.append(ask_for_the_winning_player_s_number)
            else:
                list_of_tied_players.extend(number_of_players_in_the_match)
        return list_of_winning_players, list_of_tied_players

    def score_recovery(self, json_file, number):
        """Recovery of the number of the players in the json file."""
        player_number = json_file.get("Joueur numero " + str(number), {})
        return player_number

    def score_update(self):
        """Number of points earned by players at the end of the match.

        The winning player wins 1 point.
        The losing player wins 0 point.
        In the event of a tie, each player wins 0.5 point.
        """
        final_score_of_players_at_the_end_of_the_game = {}
        recovery_of_the_json_file = players.Players().json_file_playback("players.json")
        recovery_of_player_scores_at_the_end_of_the_game = turns.Turns().creation_of_turn()
        for each_player_score in recovery_of_player_scores_at_the_end_of_the_game[0][1]:
            final_score_of_players_at_the_end_of_the_game.update({
                each_player_score[1][0]: each_player_score[1][1],
                each_player_score[2][0]: each_player_score[2][1]
            })

        for json_file_key, json_file_value in recovery_of_the_json_file.items():
            if json_file_key in final_score_of_players_at_the_end_of_the_game:
                json_file_value["Score"] += final_score_of_players_at_the_end_of_the_game[json_file_key]

        players.Players().json_file_creation("players.json", recovery_of_the_json_file)
        return recovery_of_the_json_file

    def player_ranking(self):
        """Retrieving scores from each player and ranking based on their score."""
        players_list = players.Players().json_file_playback("players.json")
        scores = {}
        for key, value in players_list.items():
            scores.update({
                key: value["Score"]
            })
        sorted_scores_list_with_values = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        return sorted_scores_list_with_values

    def selection_of_players_according_to_their_ranking(self):
        """Assign the rank of the player according to his ranking.

        If several players have the same score then they have the same rank and we skip the necessary number of ranks
        for the next.
        """
        player_ranking_list = self.player_ranking()
        score_list = []
        for value_in_player_ranking in player_ranking_list.values():
            score_list.append(value_in_player_ranking)

        sorted_scores = sorted(set(score_list), reverse=True)
        list_of_players_with_their_ranking = []
        current_rank = 1

        for score in sorted_scores:
            players_in_different_lists_according_to_their_ranking = [player for player, player_score
                                                                     in player_ranking_list.items()
                                                                     if player_score == score]
            list_of_players_with_their_ranking.extend((current_rank, player) for player
                                                      in players_in_different_lists_according_to_their_ranking)
            current_rank += len(players_in_different_lists_according_to_their_ranking)

        dictionary_with_the_rank_of_each_player = {}
        for rank, player in list_of_players_with_their_ranking:
            dictionary_with_the_rank_of_each_player.update({
                f"{player}": f"Rang {rank}"
            })
        return dictionary_with_the_rank_of_each_player

    def matches_selection_based_on_player_ranking(self):
        """Selection of matches according to the ranking of each player.

        If two players have the same rank then we draw lots to determine who will play against whom.
        """
        ranking = self.selection_of_players_according_to_their_ranking()
        rank_of_players = []
        for each_value_in_the_ranking in ranking.values():
            rank_of_players.append(each_value_in_the_ranking)

        # recovers all the ranks of all players if some have the same.
        rank_list = sorted(set(rank_of_players))
        number_of_players_ranked_according_to_their_rank = []
        for each_rank in rank_list:
            several_lists_with_in_each_the_list_of_players_with_the_same_rank = \
                [ranking_dictionary_key for ranking_dictionary_key, ranking_dictionary_value in ranking.items()
                 if ranking_dictionary_value == each_rank]
            mix_of_players_with_the_same_rank = \
                random.sample(several_lists_with_in_each_the_list_of_players_with_the_same_rank,
                              len(several_lists_with_in_each_the_list_of_players_with_the_same_rank))
            number_of_players_ranked_according_to_their_rank.extend([each_player for each_player
                                                                     in mix_of_players_with_the_same_rank])
        return number_of_players_ranked_according_to_their_rank

    def selection_of_players_who_will_play_together_according_to_their_ranking(self):
        """Selection of players to play together."""
        matches_list = []
        for each_player in range(0, len(self.matches_selection_based_on_player_ranking()), 2):
            matches_list.append(self.matches_selection_based_on_player_ranking()[each_player:each_player + 2])
        return matches_list

    def recovery_of_players_who_will_play_together_according_to_their_ranking(self):
        """Recovery of player numbers."""
        list_of_player_numbers = []
        for each_player in self.matches_selection_based_on_player_ranking():
            player_number = re.findall(r"[0-9]", each_player)
            list_of_player_numbers.extend(player_number)
        return list_of_player_numbers

    def recovery_of_players_who_have_already_played_together(self):
        """Recovering of the list of players who have already played against each other."""
        player_numbers_who_will_play_together = []
        for each_number in self.selection_of_players_who_will_play_together_according_to_their_ranking():
            first_player = re.findall(r"[0-9]", each_number[0])
            second_player = re.findall(r"[0-9]", each_number[1])
            player_numbers_who_will_play_together.append(first_player + second_player)

        json_file_recovery_to_find_out_which_players_have_already_played_together = \
            players.Players().json_file_playback("matches.json")
        player_numbers_who_have_already_played_together = []
        for each_value in json_file_recovery_to_find_out_which_players_have_already_played_together.values():
            for each_player_who_played_together in each_value.values():
                recovery_of_player_numbers = re.findall(r"[0-9]", each_player_who_played_together)
                player_numbers_who_have_already_played_together.append(recovery_of_player_numbers)

        list_of_players_who_have_already_played_together = []
        for num_actuel in player_numbers_who_have_already_played_together:
            if num_actuel in player_numbers_who_will_play_together \
                    or num_actuel[::-1] in player_numbers_who_will_play_together:
                list_of_players_who_have_already_played_together.append(num_actuel)
        return list_of_players_who_have_already_played_together

    def change_of_players_playing_together(self):
        """New list of players who will play together after retrieving the list of players who have already played
        against each other.
        """
        players_who_have_already_played_against_each_other = \
            self.recovery_of_players_who_have_already_played_together()
        list_with_player_ranking = self.recovery_of_players_who_will_play_together_according_to_their_ranking()
        list_with_modified_player_ranking = []
        index_of_each_player_in_the_list = []
        for each_pair_of_players in players_who_have_already_played_against_each_other:
            for each_player in each_pair_of_players:
                index_of_player = list_with_player_ranking.index(each_player)
                index_of_each_player_in_the_list.append(index_of_player)

        if index_of_each_player_in_the_list[0] < index_of_each_player_in_the_list[1]:
            index_of_the_next_player_in_the_list = index_of_each_player_in_the_list[0] + 1
            index_of_the_player_who_has_already_played_against_the_previous_one = \
                index_of_the_next_player_in_the_list + 1
            deletion_of_the_player_from_the_list_to_add_it_elsewhere = \
                list_with_player_ranking.pop(index_of_the_player_who_has_already_played_against_the_previous_one)
            list_with_player_ranking.insert(index_of_the_next_player_in_the_list,
                                            deletion_of_the_player_from_the_list_to_add_it_elsewhere)
        else:
            index_of_the_next_player_in_the_list = index_of_each_player_in_the_list[1] + 1
            index_of_the_player_who_has_already_played_against_the_previous_one = \
                index_of_the_next_player_in_the_list + 1
            deletion_of_the_player_from_the_list_to_add_it_elsewhere = \
                list_with_player_ranking.pop(index_of_the_player_who_has_already_played_against_the_previous_one)
            list_with_player_ranking.insert(index_of_the_next_player_in_the_list,
                                            deletion_of_the_player_from_the_list_to_add_it_elsewhere)

        for each_player in range(0, len(list_with_player_ranking), 2):
            list_with_modified_player_ranking.append(list_with_player_ranking[each_player:each_player + 2])
        return list_with_modified_player_ranking
