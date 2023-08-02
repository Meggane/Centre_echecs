import json


class Model:
    def __init__(self, json_file_data=None):
        self.json_file_data = json_file_data

    def json_file_creation(self, json_file_name, data_to_add=None):
        """Creation of the json file to retrieve the information of each player."""
        with open(f"../data/tournaments/{json_file_name}", "w") as json_file:
            json.dump(data_to_add, json_file, indent=4)

    def json_file_playback(self, json_file_name):
        """Json data recovery to manipulate and modify them if necessary."""
        with open(f"../data/tournaments/{json_file_name}") as json_file:
            self.json_file_data = json.load(json_file)
        return self.json_file_data
