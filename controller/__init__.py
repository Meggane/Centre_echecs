class InformationRetrieval:
    def __init__(self):
        self.list_of_keys_to_be_collected = []
        self.list_of_information_to_be_collected = []
        self.matches_list = []

    def retrieval_of_dictionary_keys(self, name_of_the_item_to_be_retrieved):
        """We get the keys of a given dictionary."""
        for key in name_of_the_item_to_be_retrieved:
            self.list_of_keys_to_be_collected.append(key)
        return self.list_of_keys_to_be_collected

    def retrieval_of_dictionary_values(self, dictionary_name_to_retrieve):
        """We get the values of a given dictionary."""
        for informations in dictionary_name_to_retrieve.values():
            self.list_of_information_to_be_collected.append(informations)
        return self.list_of_information_to_be_collected

    def recovery_of_players_by_two(self, list_of_players):
        """Players are added to the list in pairs. This will then create the matches."""
        for player in range(0, len(list_of_players), 2):
            self.matches_list.append(list_of_players[player:player + 2])
        return self.matches_list
