import sys

sys.path.append("..")
from controller import players
from controller import tournaments
from controller import matches
from view import reports
from view import manually_retrieve_information


class MenuConsole:
    def __init__(self):
        self.menu_console = []

    def display_menu(self, choice):
        """Menu to display with the associated number to enter."""
        self.menu_console.extend(choice)
        numbered_menu = ["\nMenu :"]
        for choice_number, choice_list in zip(range(0, len(self.menu_console)), self.menu_console):
            numbered_menu.append(f"{choice_number + 1}. {choice_list}")
        return numbered_menu

    def get_user_choice_for_menu(self):
        """Choose from the menu."""
        choice_of_menu = input("Entrez votre choix : ")
        return choice_of_menu

    def display_the_return_message(self, menu_wording):
        """Message to display after selecting the menu.
        The message indicates the menu select and the key to enter if you want to return to the main menu.
        """
        back_to_previous_menu_message = \
            f"\n{menu_wording.upper()} (Utilisez la commande Ctrl+C pour revenir au menu principal): "
        return back_to_previous_menu_message

    def back_to_previous_menu(self):
        """We delete the already established menu and we launch it again to return to the previous menu."""
        self.menu_console.clear()
        self.perform_action()

    def perform_action(self):
        """Action to be performed that the user has chosen from the menu.

        We add the menu labels and we get the user’s choice. If the user makes an error in the input, a message is
        displayed to indicate the error and he can restart the menu.
        """
        main_menu_to_add = ["Ajouter des joueurs", "Créer un tournoi", "Début du match", "Fin du match",
                            "Générer un rapport", "Quitter le programme"]
        reports_menu_to_add = ["Liste de tous les joueurs", "Liste de tous les tournois", "Nom et date d'un tournoi",
                               "Liste des joueurs d'un tournoi", "Rounds et matchs d'un tournoi"]
        for menu_wording in self.display_menu(main_menu_to_add):
            print(menu_wording)
        try:
            choice_selected_by_the_user = self.get_user_choice_for_menu()
            back_to_main_menu = self.display_the_return_message(main_menu_to_add[int(choice_selected_by_the_user) - 1])
            match choice_selected_by_the_user:
                case "1":
                    print(back_to_main_menu)
                    players.Players().add_players()
                    self.back_to_previous_menu()
                case "2":
                    print(back_to_main_menu)
                    tournaments.Tournaments().creation_of_tournament()
                    self.back_to_previous_menu()
                case "3":
                    print(back_to_main_menu)
                    matches.Matches().creation_of_round()
                    self.back_to_previous_menu()
                case "4":
                    print(back_to_main_menu)
                    tournaments.Tournaments().modification_of_the_list_of_rounds()
                    self.back_to_previous_menu()
                case "5":
                    print(back_to_main_menu)
                    self.menu_console.clear()
                    for reports_menu_wording in self.display_menu(reports_menu_to_add):
                        print(reports_menu_wording)
                    new_choice_selected_by_the_user = self.get_user_choice_for_menu()
                    match new_choice_selected_by_the_user:
                        case "1":
                            print(back_to_main_menu)
                            for each_player in reports.Reports().list_of_players_in_alphabetical_order():
                                print(each_player)
                        case "2":
                            print(back_to_main_menu)
                            for each_tournament in reports.Reports().list_of_all_tournaments():
                                print(each_tournament)
                        case "3":
                            print(back_to_main_menu)
                            for tournament_elements in reports.Reports().name_and_date_of_a_given_tournament(
                                    manually_retrieve_information.ManuallyRetrieveInformation().
                                    recovery_of_the_tournament_name()):
                                print(tournament_elements)
                        case "4":
                            print(back_to_main_menu)
                            for tournament_elements in reports.Reports().list_of_players_in_a_given_tournament(
                                    manually_retrieve_information.ManuallyRetrieveInformation().
                                    recovery_of_the_tournament_name()):
                                print(tournament_elements)
                        case "5":
                            print(back_to_main_menu)
                            for tournament_elements in reports.Reports().rounds_and_matches_of_a_given_tournament(
                                    manually_retrieve_information.ManuallyRetrieveInformation().
                                    recovery_of_the_tournament_name()):
                                print(tournament_elements)
                        case _:
                            print("Choix non valide. Veuillez réessayer")
                    self.back_to_previous_menu()
                case "6":
                    print("Fin du programme")
                case _:
                    print("Choix non valide. Veuillez réessayer")
                    self.back_to_previous_menu()
        except KeyboardInterrupt:
            print("Une erreur est survenue lors de la saisie. Veuillez réessayer")
            self.back_to_previous_menu()
        except IndexError:
            print("Une erreur est survenue lors de la saisie. Veuillez réessayer")
            self.back_to_previous_menu()
