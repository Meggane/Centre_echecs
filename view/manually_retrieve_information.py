import datetime
import re


class ManuallyRetrieveInformation:
    def __init__(self):
        self.family_name = []
        self.first_name = []
        self.date_of_birth = []

    def player_s_family_name(self):
        """Manually enter the player’s family name.

        Check if characters are only alphabetic.
        """
        ask_family_name = input("Nom de famille : ")
        if re.findall(r"[^a-zA-Z-\séèîïÉÎÏ+]", ask_family_name) or len(ask_family_name) < 2:
            print("Le nom n'est pas correct. Veuillez réessayer")
            self.family_name.append(False)
        else:
            self.family_name.append(ask_family_name)
        return self.family_name

    def player_s_first_name(self):
        """Manually enter the player’s first name.

        Check if characters are only alphabetic.
        """
        ask_first_name = input("Prénom : ")
        if re.findall(r"[^a-zA-Z-\séèîïÉÎÏ+]", ask_first_name) or len(ask_first_name) < 2:
            print("Le prénom n'est pas correct. Veuillez réessayer")
            self.first_name.append(False)
        else:
            self.first_name.append(ask_first_name)
        return self.first_name

    def player_s_date_of_birth(self):
        """Manually enter the player’s date of birth.

        Check if the input is the date type.
        """
        ask_date_of_birth = input("Date de naissance (JJ/MM/AAAA) : ")
        try:
            if datetime.datetime.strptime(ask_date_of_birth, "%d/%m/%Y"):
                self.date_of_birth.append(ask_date_of_birth)
        except ValueError:
            print("La date de naissance n'est pas au format JJ/MM/AAAA. Veuillez réessayer")
            self.date_of_birth.append(False)
        return self.date_of_birth

    def adding_a_new_player(self):
        """Ask if the user wants to add a new player."""
        next_player = input("Voulez-vous ajouter un autre joueur (o/n) : ")
        return next_player

    def know_who_won_at_the_end_of_the_round(self, first_player, second_player):
        """Ask the user if there was a winner in the round."""
        ask_match_result = input(f"Joueur numéro {first_player} contre Joueur numéro {second_player} | Y a t-il un "
                                 f"gagnant ? (o/n)")
        return ask_match_result

    def know_the_winning_player_s_number(self):
        """Ask the user for the winning player’s number."""
        ask_for_the_winning_player_s_number = input("Numéro du joueur gagnant : ")
        return ask_for_the_winning_player_s_number

    def recovery_of_the_tournament_name(self):
        """Ask the user for the name of the tournament whose information he wants to retrieve."""
        ask_for_the_name_of_the_tournament = input("Nom du tournoi à sélectionner : ")
        return ask_for_the_name_of_the_tournament
