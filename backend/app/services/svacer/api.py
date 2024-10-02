import os
import requests
from dotenv import load_dotenv


class Svacer:
    def __init__(self):
        load_dotenv('.env')
        self.server = os.environ['SVACER_SERVER']
        self.user = os.environ['SVACER_USER']
        self.password = os.environ['SVACER_PASSWORD']
        self.token = self.get_token(self.server, self.user, self.password)

    def get_token(self, server: str, user: str, password: str):

        response = requests.post(f'{server}/api/public/login',
                                 json={'login': user, 'password': password})
        if 'error' in response.json():
            raise Exception(
                f"Fail connect to svacer: {response.json()['error']}")
        return response.json()['token']

    def get_projects(self):
        response = requests.get(f'{self.server}/api/public/projects',
                                headers={"Authorization": f"Bearer {self.token}"})
        return response.json()

    def get_snapshots(self, project_id, branch_id):
        response = requests.get(f'{self.server}/api/public/projects/{project_id}/branch/{branch_id}/snapshots',
                                headers={"Authorization": f"Bearer {self.token}"})
        return response.json()

    def get_project_and_branch_ids(self, project_name, branch_name):
        projects = self.get_projects()
        project_id = ''
        branch_id = ''

        for note in projects:
            if note['project']['name'] == project_name:
                project_id = note['project']['id']
                for branch in note['branches']:
                    if branch['name'] == branch_name:
                        branch_id = branch['id']

        assert project_id, f"project id not found: {project_name}"
        assert branch_id, f"branch id not found: {branch_name}"
        return {'project_id': project_id, 'branch_id': branch_id}

    def get_snapshot_id(self, project_id, branch_id, snapshot_name):
        snapshots = self.get_snapshots(project_id, branch_id)
        snapshot_id = ''
        for snapshot in snapshots:
            if snapshot['name'] == snapshot_name:
                snapshot_id = snapshot['id']
        assert snapshot_id, f"snapshot id not found: {snapshot_name}"
        return snapshot_id

    def export_snapshot_markers_by_names(self, project_name: str, branch_name: str, snapshot_name: str):
        ids = self.get_project_and_branch_ids(project_name, branch_name)
        project_id = ids['project_id']
        branch_id = ids['branch_id']
        snapshot_id = self.get_snapshot_id(
            project_id, branch_id, snapshot_name)

        response = requests.get(f"{self.server}/api/public/projects/{project_id }/branch/{branch_id}/snapshots/{snapshot_id}/fullmarkers",
                                headers={"Authorization": f"Bearer {self.token}"}, params={'checker_info': 'true'})
        return response.json()

    def export_snapshot_markers_by_ids(self, project_id: str, branch_id: str, snapshot_id: str):
        response = requests.get(f"{self.server}/api/public/projects/{str(project_id) }/branch/{str(branch_id)}/snapshots/{str(snapshot_id)}/fullmarkers",
                                headers={"Authorization": f"Bearer {self.token}"}, params={'checker_info': 'true'})
        return response.json()
