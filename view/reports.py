import re
import sys

sys.path.append("..")
from controller import players
from model import model

TOURNAMENTS_LIST = model.Model().json_file_playback("tournaments.json")


class Reports:
    def __int__(self):
        pass

    def list_of_players_in_alphabetical_order(self):
        """Display the list of players in alphabetical order by last name."""
        list_of_players_in_alphabetical_order = players.Players().sort_players_alphabetically()
        print("Liste de tous les joueurs par ordre alphabétique :")
        for player in list_of_players_in_alphabetical_order:
            print(player)

    def list_of_all_tournaments(self):
        """Display the list of all tournaments with all related information."""
        print("Liste de tous les tournois : \n")
        for tournament_number, tournament_information in TOURNAMENTS_LIST.items():
            print(tournament_number)
            for wording in tournament_information:
                if wording == "Liste des tours":
                    print("Liste des tours :")
                    # Check if the tournament has not started yet
                    if type(tournament_information["Liste des tours"]) == str:
                        print(tournament_information["Liste des tours"])
                    else:
                        for tournament_round, tournament_round_information in tournament_information["Liste des tours"].items():
                            print(tournament_round)
                            for dictionary_key, dictionary_value in tournament_round_information.items():
                                print(f"{dictionary_key} : {dictionary_value}")
                elif wording == "Liste des joueurs":
                    print("Liste des joueurs :")
                    for player, score in tournament_information["Liste des joueurs"].items():
                        print(f"{player} : {score}")
                else:
                    print(f"{wording} : {tournament_information[f'{wording}']}")
            print()

    def name_and_date_of_a_given_tournament(self, tournament_name):
        """Display the name and date of the chosen tournament."""
        for tournament_information in TOURNAMENTS_LIST.values():
            if tournament_information["Nom du tournoi"] == tournament_name:
                print(f"Nom du tournoi : {tournament_name}")
                print(f"Date de début du tournoi : {tournament_information['Date de début du tournoi']}")
                print(f"Date de fin du tournoi : {tournament_information['Date de fin du tournoi']}")

    def list_of_players_in_a_given_tournament(self, tournament_name):
        """Display the family and first names of players in a given tournament. Players are sorted alphabetically."""
        for tournament_information in TOURNAMENTS_LIST.values():
            if tournament_information["Nom du tournoi"] == tournament_name:
                print("Liste des joueurs :")
                list_of_players = []
                for player in tournament_information["Liste des joueurs"]:
                    recovery_of_the_players_family_and_first_names = re.findall(r"[A-Za-z]+", player)
                    family_name = recovery_of_the_players_family_and_first_names[-2]
                    first_name = recovery_of_the_players_family_and_first_names[-1]
                    list_of_players.append(f"{family_name} {first_name}")
                sorting_of_players = sorted(list_of_players)
                for player_in_alphabetical_order in sorting_of_players:
                    print(player_in_alphabetical_order)

    def rounds_and_matches_of_a_given_tournament(self, tournament_name):
        """Display the list of all rounds of the tournament and all matches of the round.

        We find the players' scores, the start and end date and time as well as the color of the pieces used by the
        players.
        """
        for tournament_information in TOURNAMENTS_LIST.values():
            if tournament_information["Nom du tournoi"] == tournament_name:
                print("Liste des tours : \n")
                for round_number, round_information in tournament_information["Liste des tours"].items():
                    print(round_number)
                    for wording, indication_of_the_wording in round_information.items():
                        if wording == "Couleur des pièces des joueurs des matchs":
                            print(f"{wording} :")
                            for player_number, color_of_the_pieces in indication_of_the_wording.items():
                                print(f"{player_number} : {color_of_the_pieces}")
                        else:
                            print(f"{wording} : {indication_of_the_wording}")
                    print()
