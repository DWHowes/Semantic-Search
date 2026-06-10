import os
import json

JSON_NAME = "ssrecent.json"
MAX_FILES = 10

class RecentFiles:
    def __init__(self, run_directory: str) -> None:
        # Enforce strict path resolution to prevent chdir relative lookups from breaking state
        self.storage_path = os.path.abspath(os.path.join(run_directory, JSON_NAME))
        self.file_list = self._load_recent_files()

    def _load_recent_files(self) -> list:
        if os.path.isfile(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def add_recent_file(self, file_path: str) -> None:
        # Standardize path slashes for clean lookup checks
        normalized_path = os.path.normpath(file_path)
        
        if normalized_path in self.file_list:
            self.file_list.remove(normalized_path)
            
        self.file_list.insert(0, normalized_path)
        self.file_list = self.file_list[:MAX_FILES]

    def save_recent_file_list(self) -> None:
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as file:
                json.dump(self.file_list, file, indent=2)
        except IOError as e:
            print(f"Failed to record history manifest: {e}")

    def get_recent_file_list(self) -> list:
        return self.file_list
