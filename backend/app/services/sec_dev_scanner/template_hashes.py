import sys
import argparse
import json
import requests
import os
from datetime import datetime

from app.adapters.hasher import Hasher


class CustomHelpFormatter(argparse.HelpFormatter):
    def _get_help_string(self, action):
        help = action.help
        if '%(default)' in help:
            help = help.replace(' (default: %(default)s)', '')
        return help


parser = argparse.ArgumentParser()

parser.add_argument('-pn', '--project_name', type=str, metavar='', default='',
                    help="""Название проекта на сервере VulnScanC
Используется для указания указания проекта в выходных документах, json файлах и при отправке данных
Пример ввода: -pn=project_name""")
parser.add_argument('-sa', '--server_address', type=str, metavar='', default='',
                    help="""ip адрес и порт сервера VulnScanC, которому нужно отправить результаты
                    Например -su='127.0.0.1:5000' """)
parser.add_argument('-om', '--output_mode', type=str, metavar='', default='console',
                    help="""(Опционально) Режим вывода данных: console, file, json. По умолчанию используется console
Можно указать несколько режимов одновременно:
--output-mode=console/file/json""")
parser.add_argument('-p', '--path', type=str, metavar='', default='.',
                    help="""(Опционально) Директория для выполнения операций. По умолчанию используется текущая директория.  
Для изменения директории введите:
--path='./path/to/dir'""")

args = parser.parse_args()


def check_argument_rules():
    error_messages = []

    if not args.project_name:
        error_messages.append(
            'Укажите название проекта')

    if not args.server_address:
        error_messages.append(
            'Укажите URL сервера для отправки данных')

    if error_messages:
        print("Некорректное указание аргументов:")
        for error in error_messages:
            print(error)
        sys.exit(1)


check_argument_rules()


def collect_hashes(root_directory: str) -> list:
    extensions = (".hpp", ".h", ".hh", ".cc", ".c", ".cpp")
    hasher = Hasher()

    all_directories = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        all_directories.append(dirpath)

    hashes = []
    for directory in all_directories:
        data = hasher.hash_directory(directory, extensions)
        if not data['file_hashes']:
            continue
        hashes.append({
            'directory': directory,
            'file_hashes': data['file_hashes']
        })

    return hashes


try:
    hashes = collect_hashes(args.path)
except Exception as exc:
    url = f'http://{args.server_address}/save_hashes'
    json_to_send = {'status': 'fail',
                    'project_name': args.project_name}
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=json_to_send)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error when send results:",
              response.status_code, response.text)
    sys.exit(1)

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%d_%m_%Y_%H_%M')

if 'json' in args.output_mode:
    with open(f'{args.project_name}_hashes_{formatted_datetime}.json', 'w') as file:
        json.dump(hashes, file, indent=4, ensure_ascii=False)

if 'console' in args.output_mode:
    print(f"Collected hashes for {len(hashes)} directories")

url = f'http://{args.server_address}/save_hashes'
json_to_send = {
    'status': 'ok',
    'project_name': args.project_name,
    'datetime': formatted_datetime,
    'hashes': hashes,
    'process': True
}
headers = {
    "Content-Type": "application/json"
}
response = requests.post(url, headers=headers, json=json_to_send)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error when send results:", response.status_code, response.text)
    sys.exit(1)
