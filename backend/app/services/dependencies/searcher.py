import os
import time
import copy
from app.adapters.hasher import Hasher
from app.adapters.osv_client import OsvClient


class Searcher:
    def __init__(self):
        self.hasher = Hasher()
        self.osv_client = OsvClient()

    def search_match(self, directory: str, extensions: tuple) -> dict:
        data = self.hasher.hash_directory(directory, extensions)
        if not data['file_hashes']:
            return False

        time.sleep(0.1)
        print(f'\rrequest for search {directory}', end='', flush=True)
        MAX_RETRIES = 5
        WAIT_TIME_BASE = 30
        try:
            response = self.osv_client.determine_version(data)
        except Exception as exc:
            print(f"Initial request failed with exception: {exc}")
            for i in range(MAX_RETRIES):
                try:
                    wait_time = WAIT_TIME_BASE * (i + 1)
                    print(
                        f"Attempt {i + 1}/{MAX_RETRIES}, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    print("Retrying the request...")
                    response = self.osv_client.determine_version(data)
                    print("Request succeeded")
                    break
                except Exception as retry_exc:
                    print(f"Attempt {i + 1} failed: {retry_exc}")
                    if i == MAX_RETRIES - 1:
                        print("All retry attempts failed. Raising exception.")
                        raise retry_exc

        if not 'matches' in response:
            return False

        score = 0
        larger_score_match = ''
        for match in response['matches']:
            if match['score'] >= score:
                score = match['score']
                larger_score_match = match
        return larger_score_match

    def search_all_matches(self, root_directory: str) -> list:
        extensions = (".hpp", ".h", ".hh", ".cc", ".c", ".cpp")

        all_directories = []
        for dirpath, dirnames, filenames in os.walk(root_directory):
            all_directories.append(dirpath)

        dirs_matches_list = []
        for directory in all_directories:
            match = self.search_match(directory, extensions)
            if not match:
                continue
            dirs_matches_list.append({'directory': directory, 'match': match})

        repos_list = []
        for note in dirs_matches_list:
            if note['match']['repo_info']['address'] not in repos_list:
                repos_list.append(note['match']['repo_info']['address'])

        repos_dict = {}
        for i in repos_list:
            repos_dict[i] = []

        for note in dirs_matches_list:
            repos_dict[note['match']['repo_info']['address']].append(note)

        result = []
        for note in repos_dict:
            score = 0
            note_to_add = ''
            for i in repos_dict[note]:
                if i['match']['score'] >= score:
                    score = i['match']['score']
                    note_to_add = i
            result.append(note_to_add)
        return result
