import sys
import argparse
import json
import requests
from datetime import datetime


from app.services.dependencies.matches_osv_finder import search_all_matches
from app.services.vulnerabilities.vuln_osv_finder import search_vulnerabilities
from app.services.results.result_handler import handle_vulns, handle_matches


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
parser.add_argument('-pi', '--pipeline_id', type=str, metavar='', default='',
                    help="""ID пайплайна в GitLab""")
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

    if not args.pipeline_id:
        error_messages.append(
            'Укажите pipeline id GitLab')

    if error_messages:
        print("Некорректное указание аргументов:")
        for error in error_messages:
            print(error)
        sys.exit(1)


check_argument_rules()


try:
    matches = search_all_matches(args.path)
except:
    url = f'http://{args.server_address}/search_data'
    json_to_send = {'status': 'fail',
                    'pipeline_id': args.pipeline_id,
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

vulns = search_vulnerabilities(matches)


current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%d_%m_%Y_%H_%M')

if 'json' in args.output_mode:
    with open(f'{args.project_name}_dependencies_{formatted_datetime}.json', 'w') as file:
        json.dump(matches, file, indent=4)
    with open(f'{args.project_name}_vulnerabilities_{formatted_datetime}.json', 'w') as file:
        json.dump(vulns, file, indent=4)

if 'console' in args.output_mode:
    handle_matches(matches, output_mode='console')
    handle_vulns(vulns, output_mode='console')

if 'file' in args.output_mode:
    handle_matches(matches, output_mode='file',
                   output_file=f'{args.project_name}_dependencies_{formatted_datetime}.txt')
    handle_vulns(vulns, output_mode='file',
                 output_file=f'{args.project_name}_vulnerabilities_{formatted_datetime}.txt')


url = f'http://{args.server_address}/search_data'
# Отправить json в формате {"project_name": ...,"datetime": 13_08_2024_17_00,  "dependencies": ..., "vulnerabilities": ...}
json_to_send = {'status': 'ok',
                'pipeline_id': args.pipeline_id,
                'project_name': args.project_name,
                'datetime': formatted_datetime,
                'dependencies': matches,
                'vulnerabilities': vulns}
headers = {
    "Content-Type": "application/json"
}
response = requests.post(url, headers=headers, json=json_to_send)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error when send results:", response.status_code, response.text)
    sys.exit(1)
