import json
import re
import datetime
import os
import random


class Players:
    def __init__(self):
        self.family_name = []
        self.first_name = []
        self.date_of_birth = []
        self.list_of_all_player_numbers = []

    def add_players(self, add_new_player="o", player_number=0, score=0):
        """Add players to the tournament with the control terminal

        Manually enter family_name, first_name and date_of_birth

        The number of each player is added automatically
        """
        dictionary_of_all_players = {}
        while add_new_player == "o":
            ask_family_name = input("Nom de famille : ")
            if re.search("[^a-zA-Z]", ask_family_name) or len(ask_family_name) < 2:
                print("Le nom n'est pas correct. Veuillez réessayer")
                break
            else:
                self.family_name.append(ask_family_name)

            ask_first_name = input("Prénom : ")
            if re.search("[^a-zA-Z]", ask_first_name) or len(ask_first_name) < 2:
                print("Le prénom n'est pas correct. Veuillez réessayer")
                break
            else:
                self.first_name.append(ask_first_name)

            ask_date_of_birth = input("Date de naissance (JJ/MM/AAAA) : ")
            try:
                if datetime.datetime.strptime(ask_date_of_birth, "%d/%m/%Y"):
                    self.date_of_birth.append(ask_date_of_birth)
            except ValueError:
                print("La date de naissance n'est pas au format JJ/MM/AAAA. Veuillez réessayer")
                break

            player_number += 1
            self.list_of_all_player_numbers.append(player_number)

            for each_player_number, each_family_name, each_first_name, each_date_of_birth \
                    in zip(self.list_of_all_player_numbers, self.family_name, self.first_name, self.date_of_birth):
                dictionary_of_all_players.update({
                    "Joueur numero " + str(each_player_number): {
                        "Nom de famille": each_family_name,
                        "Prenom": each_first_name,
                        "Date de naissance": each_date_of_birth,
                        "Score": score
                    },
                })

            next_player = input("Voulez-vous ajouter un autre joueur (o/n) : ")
            if next_player != "o":
                break
        return dictionary_of_all_players

    def json_file_creation(self, data_to_add=None):
        """Creation of the json file to retrieve the information of each player

        If the json file doesn't exist then it's created with the add_players function otherwise the file is modified
        """
        if not os.path.isfile("players.json"):
            data_to_add = self.add_players()

        with open("players.json", "w") as json_file:
            json.dump(data_to_add, json_file, indent=4)

    def json_file_playback(self):
        """Json data recovery to manipulate and modify them if necessary"""
        with open("players.json") as json_file:
            json_file_data = json.load(json_file)
        return json_file_data

    def randomly_mix_players(self):
        """Randomly mix players to create random matches for the first game"""
        players_list = list(self.json_file_playback())
        mix_of_players = random.sample(players_list, len(players_list))
        return mix_of_players

    def random_player_selection(self):
        """Define players who play together according to the random list of players"""
        mixed_list_players = self.randomly_mix_players()
        matches_list = []
        for each_player in range(0, len(mixed_list_players), 2):
            matches_list.append(mixed_list_players[each_player:each_player + 2])
        return matches_list
