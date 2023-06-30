import re
import players
import turns


list_of_winning_players = []
list_of_tied_players = []


class Match:
    def __int__(self):
        self.player_score = []

    def end_of_game_result(self):
        """Recovery of winning player and tied player numbers"""
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
        """Recovery of the number of the players in the json file"""
        player_number = json_file.get("Joueur numero " + str(number), {})
        return player_number

    def score_update(self):
        """Number of points earned by players at the end of the match

        The winning player wins 1 point
        The losing player wins 0 point
        In the event of a tie, each player wins 0.5 point
        """
        final_score_of_players_at_the_end_of_the_game = {}
        recovery_of_the_json_file = players.Players().json_file_playback()
        recovery_of_player_scores_at_the_end_of_the_game = turns.Turns().creation_of_turn()
        for each_player_score in recovery_of_player_scores_at_the_end_of_the_game[0][1]:
            final_score_of_players_at_the_end_of_the_game.update({
                each_player_score[1][0]: each_player_score[1][1],
                each_player_score[2][0]: each_player_score[2][1]
            })

        for json_file_key, json_file_value in recovery_of_the_json_file.items():
            if json_file_key in final_score_of_players_at_the_end_of_the_game:
                json_file_value["Score"] += final_score_of_players_at_the_end_of_the_game[json_file_key]

        players.Players().json_file_creation(recovery_of_the_json_file)

        return recovery_of_the_json_file
