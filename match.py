import random
import players


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
