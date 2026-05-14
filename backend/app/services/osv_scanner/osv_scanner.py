import time
import copy
from app.adapters.osv_client import OsvClient, calculate_severities


class OSVScanner:
    def __init__(self):
        self.osv_client = OsvClient()

    def process_hashes(self, hashes: list) -> list:
        """
        Принимает список директорий с хешами в формате:
        [
            {
                "directory": "/path/to/dir",
                "file_hashes": [{"hash": "...", "file_path": "..."}]
            }
        ]
        Возвращает результат в формате matches + vulns, совместимом с SearchDataService:
        [
            {
                "directory": "/path/to/dir",
                "match": {...},
                "vulns": [...]
            }
        ]
        """
        all_directories = []
        for h in hashes:
            all_directories.append({
                'directory': h['directory'],
                'file_hashes': h['file_hashes']
            })

        dirs_matches_list = []
        for directory_data in all_directories:
            match = self._determine_version(directory_data)
            if not match:
                continue
            dirs_matches_list.append({
                'directory': directory_data['directory'],
                'match': match
            })

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

        matches = copy.deepcopy(result)
        vuln_result = []
        if matches:
            for i in range(len(matches)):
                response = self.osv_client.search_by_commit(
                    matches[i]['match']['repo_info']['commit'])
                if not 'vulns' in response:
                    continue
                matches[i]['vulns'] = response['vulns']
                for vuln in matches[i]['vulns']:
                    if 'severity' in vuln and 'score' in vuln['severity'][0]:
                        calculated_severities = calculate_severities(
                            vuln['severity'][0]['score'])
                        vuln['severity'][0]['calculated_severities'] = calculated_severities
                vuln_result.append(matches[i])

        return vuln_result

    def _determine_version(self, directory_data: dict) -> dict | None:
        data = {
            'name': directory_data['directory'],
            'file_hashes': directory_data['file_hashes']
        }
        if not data['file_hashes']:
            return None

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
            return None

        score = 0
        larger_score_match = ''
        for match in response['matches']:
            if match['score'] >= score:
                score = match['score']
                larger_score_match = match
        return larger_score_match
