from pathlib import Path
import os
import hashlib
import base64
import requests
import time
import hashlib
from collections import defaultdict
from dataclasses import dataclass


class Hasher:
    """Собирает локальные данные: хеши файлов и структуры директорий."""

    def __init__(self):
        self.files_extensions = (".hpp", ".h", ".hh", ".cc", ".c", ".cpp")

    @staticmethod
    def create_hash(file_path: str) -> str:
        with open(file_path, 'rb') as file:
            text = file.read()
            hash_obj = hashlib.md5(text).digest()
            base64_encoded_hash = base64.b64encode(hash_obj)
            return base64_encoded_hash.decode('utf-8')

    @staticmethod
    def find_files_with_extensions(directory: str, extensions: list) -> list:
        file_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extensions):
                    file_list.append(os.path.join(root, file))
        return file_list

    @staticmethod
    def get_all_directories(root_dir: str) -> list:
        directories = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            directories.append(dirpath)
        return directories

    @staticmethod
    def _make_relative_path(file_path: str, root_dir: str) -> str:
        dir_name, file_name = os.path.split(file_path)
        _, last_dir_name = os.path.split(dir_name)
        return os.path.join(last_dir_name, file_name)

    def prepare_request_body(self, directory: str, extensions: list) -> dict:
        file_list = self.find_files_with_extensions(directory, extensions)
        file_hashes = []
        for file in file_list:
            file_hash = self.create_hash(file)
            result_path = self._make_relative_path(file, directory)
            file_hashes.append({'hash': file_hash, 'file_path': result_path})
        return {'name': directory, 'file_hashes': file_hashes}

    def prepare_all_request_bodies(self, root_directory: str) -> list:
        directories = self.get_all_directories(root_directory)
        bodies = []
        for directory in directories:
            body = self.prepare_request_body(directory, self.files_extensions)
            if body['file_hashes']:
                bodies.append(body)
        return bodies


class OsvSearcher:
    """Опрашивает API OSV, агрегирует и возвращает лучшие совпадения."""

    API_URL = 'https://api.osv.dev/v1experimental/determineversion'
    MAX_RETRIES = 5
    WAIT_TIME_BASE = 30
    REQUEST_DELAY = 0.1

    def __init__(self, api_url: str = None, max_retries: int = None,
                 wait_time_base: int = None, request_delay: float = None):
        self.api_url = api_url or self.API_URL
        self.max_retries = max_retries if max_retries is not None else self.MAX_RETRIES
        self.wait_time_base = wait_time_base if wait_time_base is not None else self.WAIT_TIME_BASE
        self.request_delay = request_delay if request_delay is not None else self.REQUEST_DELAY

    def _send_request(self, data: dict) -> dict:
        time.sleep(self.request_delay)
        # print(f'\rrequest for search {data["name"]}', end='', flush=True)
        print(f'request for search {data["name"]}\n')
        try:
            response = requests.post(self.api_url, json=data)
        except Exception as exc:
            print(f"Initial request failed with exception: {exc}")
            for i in range(self.max_retries):
                try:
                    wait_time = self.wait_time_base * (i + 1)
                    print(
                        f"Attempt {i + 1}/{self.max_retries}, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    print("Retrying the request...")
                    response = requests.post(self.api_url, json=data)
                    print("Request succeeded")
                    break
                except Exception as retry_exc:
                    print(f"Attempt {i + 1} failed: {retry_exc}")
                    if i == self.max_retries - 1:
                        print("All retry attempts failed. Raising exception.")
                        raise retry_exc
        return response.json()

    @staticmethod
    def _best_match(matches: list) -> dict:
        score = 0
        best = None
        for match in matches:
            try:
                print(match)
                if match['score'] >= score:
                    score = match['score']
                    best = match
            except KeyError:
                print("key error:", match)
                exit(1)
        return best

    def search_match(self, data: dict) -> dict:
        if not data['file_hashes']:
            return False
        response = self._send_request(data)
        if not 'matches' in response:
            return False
        return self._best_match(response['matches'])

    def search_all_matches(self, root_directory: str) -> list:
        hasher = Hasher()
        bodies = hasher.prepare_all_request_bodies(root_directory)

        dirs_matches_list = []
        for body in bodies:
            match = self.search_match(body)
            if not match:
                continue
            dirs_matches_list.append(
                {'directory': body['name'], 'match': match})

        repos_list = []
        for note in dirs_matches_list:
            addr = note['match']['repo_info']['address']
            if addr not in repos_list:
                repos_list.append(addr)

        repos_dict = {}
        for addr in repos_list:
            repos_dict[addr] = []

        for note in dirs_matches_list:
            repos_dict[note['match']['repo_info']['address']].append(note)

        result = []
        for addr in repos_dict:
            best = self._best_match(repos_dict[addr])
            result.append(best)
        return result


@dataclass(frozen=True)
class FileHash:
    path: str
    hash: str
    size: int


@dataclass(frozen=True)
class DirectoryHash:
    path: str
    hash: str
    file_count: int
    total_size: int


class Hasher2:
    def __init__(self, extensions=None):
        self.extensions = extensions or {
            ".hpp", ".h", ".hh", ".cc", ".c", ".cpp"
        }

    @staticmethod
    def create_hash(file_path: Path) -> str:
        hash_obj = hashlib.sha256()

        with file_path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def should_scan_file(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.extensions

    def scan(self, root_dir: str) -> tuple[list[FileHash], list[DirectoryHash]]:
        root = Path(root_dir).resolve()

        file_hashes: list[FileHash] = []
        directory_items = defaultdict(list)

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if not self.should_scan_file(path):
                continue

            file_hash = self.create_hash(path)
            size = path.stat().st_size
            rel_path = path.relative_to(root).as_posix()

            file_hashes.append(
                FileHash(
                    path=rel_path,
                    hash=file_hash,
                    size=size,
                )
            )

            current_dir = path.parent

            while True:
                rel_to_current_dir = path.relative_to(current_dir).as_posix()

                directory_items[current_dir].append(
                    {
                        "relative_path": rel_to_current_dir,
                        "hash": file_hash,
                        "size": size,
                    }
                )

                if current_dir == root:
                    break

                current_dir = current_dir.parent

        directory_hashes: list[DirectoryHash] = []

        for directory, items in directory_items.items():
            dir_hash_obj = hashlib.sha256()

            total_size = 0

            for item in sorted(items, key=lambda x: x["relative_path"]):
                total_size += item["size"]

                line = (
                    item["relative_path"]
                    + "0"
                    + item["hash"]
                    + "0"
                    + str(item["size"])
                    + "\n"
                )

                dir_hash_obj.update(line.encode("utf-8"))

            directory_hashes.append(
                DirectoryHash(
                    path=directory.relative_to(root).as_posix()
                    if directory != root
                    else ".",
                    hash=dir_hash_obj.hexdigest(),
                    file_count=len(items),
                    total_size=total_size,
                )
            )

        return file_hashes, directory_hashes


# if __name__ == '__main__':
#     searcher = OsvSearcher()
#     print(searcher.search_all_matches('/home/user/test_analyze'))
hasher = Hasher2()

files, directories = hasher.scan(
    "/home/user/test_analyze/test_analyze_project")

for directory in directories:
    print(directory)
