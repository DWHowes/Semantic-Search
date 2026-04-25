import os
import json

JSON_NAME = "ssrecent.json"
MAX_FILES = 10

class RecentFiles():
    def __init__(self, dir:str)->None:
        self.file_list = self.__open_recent_files(dir)

    def __open_recent_files(self, fpath:str)->list:
        self.file_path = fpath + "\\" + JSON_NAME
        data_list = []

        if os.path.isfile(JSON_NAME):
            with open(self.file_path, 'r') as file:
                data_list = json.load(file)

        return data_list

    def add_recent_file(self, fpath:str)->None:
        max_length = MAX_FILES

        if fpath not in self.file_list:
            self.file_list.insert(0, fpath)

        self.recent_file_list = self.file_list[:max_length]

    def save_recent_file_list(self)->None:
        if len(self.file_list):
            with open(self.file_path, 'w') as file:
                json.dump(self.file_list, file)

    def get_recent_file_list(self)->list:
        return self.file_list

