import re
import match


NUMBER_OF_TURNS = 4
PLAYER_OF_EACH_MATCH = match.Match().random_player_selection()


class Turns:
    def __int__(self, tour_start_date, tour_end_date, tour_start_time, tour_end_time):
        self.tour_start_date = tour_start_date
        self.tour_end_date = tour_end_date
        self.tour_start_time = tour_start_time
        self.tour_end_time = tour_end_time

    def creation_of_match(self, score=0):
        """Creation of the list of matches with the match number, the number of players competing and the score of
        each"""
        current_list_of_matches = []
        match_number = 0
        for each_match in PLAYER_OF_EACH_MATCH:
            match_number += 1
            current_list_of_matches.append((
                    "Match " + str(match_number),
                    [each_match[0], score],
                    [each_match[1], score]
                ))
        return current_list_of_matches

    def end_of_turn_result(self):
        """Recovery of winning player and tied player numbers for each round"""
        list_of_winning_players_of_the_round = []
        list_of_tied_players_of_the_round = []
        list_of_winning_players_of_the_round.clear()
        list_of_tied_players_of_the_round.clear()

        ongoing_matches = self.creation_of_match()
        for each_match in ongoing_matches:
            first_player = each_match[1][0]
            second_player = each_match[2][0]
            number_of_players_in_the_match_1 = re.findall(r"[0-9]", first_player)
            number_of_players_in_the_match_2 = re.findall(r"[0-9]", second_player)
            ask_match_result = input(str(first_player) + " contre " + str(second_player)
                                                                    + " | Y a t-il un gagnant ? (o/n)")
            if ask_match_result == "o":
                ask_for_the_winning_player_s_number = input("Numéro du joueur gagnant : ")
                list_of_winning_players_of_the_round.append(ask_for_the_winning_player_s_number)
            else:
                list_of_tied_players_of_the_round.extend(number_of_players_in_the_match_1)
                list_of_tied_players_of_the_round.extend(number_of_players_in_the_match_2)
        return list_of_winning_players_of_the_round, list_of_tied_players_of_the_round

    def creation_of_turn(self, lap_number=1):
        """Creation of each round with the round number, the list of matches with the score of each player, the start
        and end date of the round and the start and end time of the round

        To add the score, we check the list of winners and tied players
        The winning player wins 1 point
        The losing player wins 0 point
        In the event of a tie, each player wins 0.5 point

        On each round, we delete the previous one to keep only the last round with the last score of each player
        """
        current_list_of_turns = []
        tour_end_date = False
        tour_end_time = False
        recovery_of_the_list_of_matches = self.creation_of_match()

        while lap_number <= NUMBER_OF_TURNS:
            current_list_of_turns.clear()
            tour_start_date = input("Date de début de tour : ")
            tour_start_time = input("Heure de début de tour : ")
            recovery_of_the_list_of_winning_players_and_tied_players = self.end_of_turn_result()
            list_of_winning_players = recovery_of_the_list_of_winning_players_and_tied_players[0]
            list_of_tied_players = recovery_of_the_list_of_winning_players_and_tied_players[1]

            for each_match in recovery_of_the_list_of_matches:
                list_of_matches_with_the_score = each_match[1:]
                for each_player_number in list_of_matches_with_the_score:
                    score_of_each_player = each_player_number[1]
                    for winning_player in list_of_winning_players:
                        if winning_player in each_player_number[0]:
                            score_of_each_player += 1
                    for tied_player in list_of_tied_players:
                        if tied_player in each_player_number[0]:
                            score_of_each_player += 0.5
                    each_player_number[1] = score_of_each_player
            current_list_of_turns.append(["Round " + str(lap_number), recovery_of_the_list_of_matches,
                                          ["Date de début : ", tour_start_date, "Heure de début : ", tour_start_time],
                                          ["Date de fin :", tour_end_date, "Heure de fin : ", tour_end_time]])
            lap_number += 1
        return current_list_of_turns
