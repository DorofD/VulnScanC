import json
import copy
from datetime import datetime

from app.pg_repository.queries.projects import DBProjects
from app.pg_repository.queries.components import DBComponents
from app.pg_repository.queries.vulnerabilities import DBVulnerabilities
from app.pg_repository.queries.snapshots import DBSnapshots


class SearchDataService:
    def __init__(self):
        self.db_projects = DBProjects()
        self.db_components = DBComponents()
        self.db_vulnerabilities = DBVulnerabilities()
        self.db_snapshots = DBSnapshots()

    def save_search_data(self, data: dict):
        """
        Принимает json в формате 
                {'status': 'ok',
                'pipeline_id': args.pipeline_id,
                'project_name': args.project_name,
                'datetime': formatted_datetime,
                'dependencies': matches,
                'vulnerabilities': vulns}
        """
        try:
            projects = self.db_projects.get_projects()
            project = next(
                (p for p in projects if p['name'] == data['project_name']), None)
            if not project:
                raise Exception(f"Project not found: {data['project_name']}")
            project_id = project['id']
        except Exception as e:
            if isinstance(e, Exception) and "Project not found" in str(e):
                raise e
            raise Exception(f"Error finding project: {e}")

        try:
            handled_data = self._handle_data(data)
        except Exception as exc:
            raise Exception(f"Error when handling data: {exc}")

        try:
            components = self.db_components.get_project_components(project_id)
            components_paths = [component['path'] for component in components]
            components_ids = [component['id'] for component in components]
            components_path_id_dict = {
                component['path']: component['id'] for component in components}
        except Exception as exc:
            raise Exception(f"Error fetching components: {exc}")

        try:
            # добавление компонентов
            for note in handled_data['dependencies']:
                if note['directory'] not in components_paths:
                    new_comp = self.db_components.add_component(
                        project_id=project_id,
                        path=note['directory'],
                        type=note['match']['repo_info']['type'],
                        address=note['match']['repo_info']['address'],
                        tag=note['match']['repo_info']['tag'],
                        version=note['match']['repo_info']['version'],
                        score=note['match']['score']
                    )
                    components_ids.append(new_comp['id'])
                    components_path_id_dict[note['directory']] = new_comp['id']
                    components_paths.append(note['directory'])
        except Exception as exc:
            raise Exception(f"Error when adding components: {exc}")

        try:
            # добавление уязвимостей
            vulnerabilities = self.db_vulnerabilities.get_vulnerabilities_by_components(
                components_ids)
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
                self.db_vulnerabilities.add_vulnerabilities(vulns_to_add)
        except Exception as exc:
            raise Exception(f"Error when adding vulnerabilities: {exc}")

        try:
            # создание снапшота
            date_object = datetime.strptime(
                data['datetime'], '%d_%m_%Y_%H_%M')
            datetime_str = date_object.strftime('%d.%m.%Y %H:%M')

            components_ids_snapshot = []
            for note in handled_data['dependencies']:
                components_ids_snapshot.append(
                    components_path_id_dict[note['directory']])
            components_ids_snapshot_str = ', '.join(
                map(str, components_ids_snapshot))
            self.db_snapshots.add_snapshot(
                project_id, datetime_str, components_ids_snapshot_str)
        except Exception as exc:
            raise Exception(f"Error when create snapshot: {exc}")

        return True

    def _handle_data(self, data: dict):
        """ собирает из данных dependencies и vulnerabilities единый словарь """
        handled_data = copy.deepcopy(data)

        for dependency in handled_data['dependencies']:
            for vuln in handled_data['vulnerabilities']:
                if vuln['directory'] == dependency['directory']:
                    dependency['vulnerabilities'] = vuln['vulns']
        del handled_data['vulnerabilities']
        return handled_data
