import json
import copy
from datetime import datetime

from app.repository.queries.components import get_project_components, add_component
from app.repository.queries.vulnerabilities import get_vulnerabilities_by_components, add_vulnerabilities
from app.repository.queries.projects import get_projects, get_project
from app.repository.queries.snapshots import add_snapshot


def save_search_data(data: dict):
    """
    Принимает json в формате {"project_name": ...,"datetime": 13_08_2024_17_00,  "dependencies": ..., "vulnerabilities": ...}
    """
    try:
        project_id = get_project(data['project_name'])[0]['id']
    except:
        raise Exception(f"Project not found: {data['project_name']}")

    try:
        handled_data = handle_data(data)
    except Exception as exc:
        raise Exception(f"Error when handling data: {exc}")

    components = get_project_components(project_id)
    components_paths = [component['path'] for component in components]
    components_ids = [component['id'] for component in components]
    components_path_id_dict = {
        component['path']: component['id'] for component in components}

    try:
        # добавление компонентов
        for note in handled_data['dependencies']:
            if note['directory'] not in components_paths:
                add_component(project_id=project_id, path=note['directory'],
                              type=note['match']['repo_info']['type'],
                              address=note['match']['repo_info']['address'],
                              tag=note['match']['repo_info']['tag'],
                              version=note['match']['repo_info']['version'],
                              score=note['match']['score'])
    except Exception as exc:
        raise Exception(f"Error when adding components: {exc}")

    try:
        # добавление уязвимостей
        components = get_project_components(project_id)
        components_path_id_dict = {
            component['path']: component['id'] for component in components}
        vulnerabilities = get_vulnerabilities_by_components(components_ids)
        osv_vuln_ids = [vulnerability['osv_id']
                        for vulnerability in vulnerabilities]
        vulns_to_add = []
        for note in handled_data['dependencies']:
            if 'vulnerabilities' in note:
                for vuln in note['vulnerabilities']:
                    if vuln['id'] not in osv_vuln_ids:
                        vulns_to_add.append(
                            (components_path_id_dict[note['directory']], vuln['id'], str(vuln)))
        if vulns_to_add:
            add_vulnerabilities(vulns_to_add)
    except Exception as exc:
        raise Exception(f"Error when adding vulnerabilities: {exc}")

    try:
        # создание снапшота
        date_object = datetime.strptime(
            data['datetime'], '%d_%m_%Y_%H_%M')
        datetime_str = date_object.strftime('%d.%m.%Y %H:%M')
        components = get_project_components(project_id)
        components_path_id_dict = {
            component['path']: component['id'] for component in components}
        components_ids_snapshot = []
        for note in handled_data['dependencies']:
            components_ids_snapshot.append(
                components_path_id_dict[note['directory']])
        components_ids_snapshot_str = ', '.join(
            map(str, components_ids_snapshot))
        add_snapshot(project_id, datetime_str, components_ids_snapshot_str)
    except Exception as exc:
        raise Exception(f"Error when create snapshot: {exc}")

    return True


def handle_data(data: dict):
    """ собирает из данных dependencies и vulnerabilities единый словарь """
    handled_data = copy.deepcopy(data)

    for dependency in handled_data['dependencies']:
        for vuln in handled_data['vulnerabilities']:
            if vuln['directory'] == dependency['directory']:
                dependency['vulnerabilities'] = vuln['vulns']
    del handled_data['vulnerabilities']
    return handled_data
