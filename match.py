import random
import re
import players


list_of_winning_players = []
list_of_tied_players = []


class Match:
    def __int__(self):
        self.player_score = []

    def randomly_mix_players(self):
        """Randomly mix players to create random matches for the first game"""
        players_list = list(players.Players().json_file_playback())
        mix_of_players = random.sample(players_list, len(players_list))
        return mix_of_players

    def random_player_selection(self):
        """Define players who play together according to the random list of players"""
        mixed_list_players = self.randomly_mix_players()
        matches_list = []
        for each_player in range(0, len(mixed_list_players), 2):
            matches_list.append(mixed_list_players[each_player:each_player + 2])
        return matches_list

    def end_of_game_result(self):
        """Recovery of winning player and tied player numbers"""
        ongoing_matches = self.random_player_selection()
        for each_match in ongoing_matches:
            players_in_the_match = "".join(each_match)
            number_of_players_in_the_match = re.findall(r"[0-9]", players_in_the_match)
            ask_match_result = input(" contre ".join(each_match) + " | Y a t-il un gagnant ? (o/n)")
            if ask_match_result == "o":
                ask_for_the_winning_player_s_number = input("Numéro du joueur gagnant : ")
                list_of_winning_players.append(ask_for_the_winning_player_s_number)
                number_of_players_in_the_match.remove(ask_for_the_winning_player_s_number)
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
        self.end_of_game_result()
        json_file = players.Players().json_file_playback()
        for winning_player_number in list_of_winning_players:
            winning_player = self.score_recovery(json_file, winning_player_number)
            winning_player_s_score = winning_player.get("Score", [])
            winning_player_s_score += 1
            winning_player["Score"] = winning_player_s_score
        for tied_player_number in list_of_tied_players:
            tied_player = self.score_recovery(json_file, tied_player_number)
            tied_player_s_score = tied_player.get("Score", [])
            tied_player_s_score += 0.5
            tied_player["Score"] = tied_player_s_score
        return json_file
