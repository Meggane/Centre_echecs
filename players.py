import re
import datetime


class Players:
    def __init__(self):
        self.family_name = []
        self.first_name = []
        self.date_of_birth = []

    def add_players(self, add_new_player="o"):
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

            next_player = input("Voulez-vous ajouter un autre joueur (o/n) : ")
            if next_player != "o":
                break
        return self.family_name, self.first_name, self.date_of_birth
