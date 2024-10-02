# В нашей целевой модели обработки уязвимостей dependency track не используется,
# т.к. нет возможности автоматизированно и гарантированно устанавливать версии зависимостей и их типы из-за отсутсвия пакетного менеджера.
# Данный файл - наработка на случай появления проектов, в которых будет возможность это делать

import requests

# вынести в переменные окружения
DTRACK_URL = "http://192.168.1.1:8081"
DTRACK_API_KEY = "odt_u1shJ5nnelFJLlWQBsI8IjNtxXMIZUns"


def upload_sbom(project_name):
    url = f"{DTRACK_URL}/api/v1/bom"

    headers = {
        'X-Api-Key': DTRACK_API_KEY
    }

    sbom_file_path = './services/dependencies/test_sbom.json'

    with open(sbom_file_path, 'rb') as file:
        print(file)
        files = {
            'bom': (sbom_file_path, file),
            'project': (None, get_project_uuid(project_name))
        }

        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            print("SBOM успешно импортирован")
        else:
            print(
                f"Ошибка при импорте SBOM: {response.status_code} - {response.text}")
            print(response)


def get_projects():
    url = f"{DTRACK_URL}/api/v1/project"
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': DTRACK_API_KEY
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        projects = response.json()
    else:
        print(f'Failed to retrieve projects: {response.status_code}')
        print(response.text)
    return projects


def get_project_uuid(project_name):
    projects = get_projects()
    for note in projects:
        if project_name == note['name']:
            return note['uuid']
