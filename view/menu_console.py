import sys

sys.path.append("..")
from controller import players
from controller import tournaments
from controller import matches


class MenuConsole:
    def __int__(self):
        pass

    def display_menu(self, choice):
        menu_console = []
        menu_console.extend(choice)
        print("Menu :")
        for choice_number, choice_list in zip(range(0, len(menu_console)), menu_console):
            print(f"{choice_number + 1}. {choice_list}")

    def get_user_choice_for_menu(self):
        choice_of_menu = input("Entrez votre choix : ")
        return choice_of_menu

    def perform_action(self):
        self.display_menu(["Ajouter des joueurs", "Créer un tournoi", "Début du match", "Fin du match",
                           "Générer un rapport", "Quitter le programme"])
        choice_selected_by_the_user = self.get_user_choice_for_menu()
        try:
            if choice_selected_by_the_user == "1":
                players.Players().add_players()
            elif choice_selected_by_the_user == "2":
                tournaments.Tournaments().creation_of_tournament()
            elif choice_selected_by_the_user == "3":
                matches.Matches().creation_of_round()
            elif choice_selected_by_the_user == "4":
                tournaments.Tournaments().modification_of_the_list_of_rounds()
            elif choice_selected_by_the_user == "5":
                pass
            elif choice_selected_by_the_user == "6":
                print("Fin du programme")
            else:
                print("Choix non valide. Veuillez réessayer")
        except KeyboardInterrupt:
            print("Une erreur est survenue lors de la saisie. Veuillez réessayer")
