import os
import hashlib
import base64
import requests
import time


def create_hash(file_path: str):
    with open(file_path, 'rb') as file:
        text = file.read()
        hash_obj = hashlib.md5(text).digest()
        base64_encoded_hash = base64.b64encode(hash_obj)
        encoded_string = base64_encoded_hash.decode('utf-8')
        return encoded_string


def find_files_with_extensions(directory: str, extensions: list):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                file_list.append(os.path.join(root, file))
    return file_list


def prepare_request_body(directory: str, extensions: list):
    file_list = find_files_with_extensions(directory, extensions)
    file_hashes = []
    for file in file_list:
        file_hash = create_hash(file)
        dir_name, file_name = os.path.split(file)
        _, last_dir_name = os.path.split(dir_name)
        result_path = os.path.join(last_dir_name, file_name)
        file_hashes.append({'hash': file_hash, 'file_path': result_path})

    return {'name': directory, 'file_hashes': file_hashes}


def get_all_directories(root_dir):
    directories = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        directories.append(dirpath)
    return directories


def search_match(directory: str, extensions: list):
    """ поиск наиболее подходящего совпадения для заданной директории """
    data = prepare_request_body(directory, extensions)
    if not data['file_hashes']:
        return False

    # у API, к которому идёт обращение ниже, есть лимит на кол-во запросов в секунду. На данный момент sleep решает проблему
    time.sleep(0.1)
    print(f'\rrequest for search {directory}', end='', flush=True)
    try:
        response = requests.post(
            'https://api.osv.dev/v1experimental/determineversion', json=data)
    except Exception as exc:
        print(f"Exception: {exc}")
        print(f"Try again...")
        time.sleep(300)
        print("Continuing execution...")
        print(f'request for search {directory}')
        try:
            response = requests.post(
                'https://api.osv.dev/v1experimental/determineversion', json=data)
        except Exception as exc:
            print(f"Failed attempt, shutdown, exception is: {exc}")
            raise Exception(exc)

    if not 'matches' in response.json():
        return False

    score = 0
    larger_score_match = ''
    for match in response.json()['matches']:
        if match['score'] >= score:
            score = match['score']
            larger_score_match = match
    return larger_score_match


def search_all_matches(root_directory: str):
    """
    поиск наиболее подходящих совпадений по всему проекту
    возвращает список словарей в формате [{'directory':'директория библиотеки в проекте', 'match':'наиболее точное совпадение'}, ...]
    """
    extensions = (".hpp", ".h", ".hh", ".cc", ".c", ".cpp")

    all_directories = get_all_directories(root_directory)
    dirs_matches_list = []
    for directory in all_directories:
        match = search_match(directory, extensions)
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
