import requests
import os
from dotenv import load_dotenv


class DT:
    def __init__(self):
        load_dotenv('.env')
        self.dt_server = os.environ['DTRACK_URL']
        self.api_key = os.environ['DTRACK_API_KEY']

    def get_projects(self):
        url = f"{self.dt_server}/api/v1/project"
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            projects = response.json()
        else:
            print(f'Failed to retrieve projects: {response.status_code}')
            print(response.text)
            return False
        return projects

    def get_project_components(self, project_uuid):
        url = f"{self.dt_server}/api/v1/component/project/{project_uuid}"
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
        }
        params = {"offset": 0, "limit": 200}
        components = []
        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                if not response.json():
                    break
                components += response.json()
                params['offset'] += params['limit']
            else:
                raise Exception(
                    f"Failed to retrieve components: {response.status_code}")
        return components

    def get_component_vulnerabilities(self, component_uuid):
        url = f"{self.dt_server}/api/v1/vulnerability/component/{component_uuid}"
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            vulnerabilities = response.json()
        else:
            raise Exception(
                f"Failed to retrieve component vulnerabilities: {response.status_code}")
        return vulnerabilities

    def get_project_vulnerabilities(self, project_uuid):
        url = f"{self.dt_server}/api/v1/vulnerability/project/{project_uuid}"
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            vulnerabilities = response.json()
        else:
            raise Exception(
                f"Failed to retrieve project vulnerabilities: {response.status_code}")
        return vulnerabilities

    def get_component_info(self, component_uuid):
        url = f"{self.dt_server}/api/v1/component/{component_uuid}"
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            component_info = response.json()
        else:
            raise Exception(
                f"Failed to retrieve component info: {response.status_code}")
        return component_info

    def get_project_info(self, project_uuid):
        url = f"{self.dt_server}/api/v1/project/{project_uuid}"
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            project_info = response.json()
        else:
            raise Exception(
                f"Failed to retrieve component info: {response.status_code}")
        return project_info

    def get_vulnerable_project_components(self, project_uuid):
        project_vulns = self.get_project_vulnerabilities(project_uuid)
        vulnerable_components_uuids = []
        for vuln in project_vulns:
            for component in vuln['components']:
                vulnerable_components_uuids.append(component['uuid'])
        vulnerable_components_uuids = set(vulnerable_components_uuids)

        vulnerable_components = []
        for uuid in vulnerable_components_uuids:
            vulnerable_components.append(self.get_component_info(uuid))
        for component in vulnerable_components:
            component['vulnerabilities'] = self.get_component_vulnerabilities(
                component['uuid'])

        return vulnerable_components


# dt = DT()
# projects = dt.get_projects()
# # print(projects[0]['uuid'])

# vuln_components = dt.get_vulnerable_project_components(
#     '85cb8623-4343-4a1c-ab03-a15a0310367d')

# for i in vulns:
#     for s in i['components']:
#         for f in s:
#             print(f)
#     break

# проект 85cb8623-4343-4a1c-ab03-a15a0310367d
# vulns = dt.get_component_vulnerabilities(
#     '4350eedc-53cf-4c28-bee9-31bd5bf6ae75')


# компоненты без set, т.е. в некоторых компонентах по 2 уязвимости
# 2fa898e1-9427-4ffa-ade9-f10a9c034662
# 3e382101-a983-4ab3-a7d9-35bfc73a734a
# 3e382101-a983-4ab3-a7d9-35bfc73a734a
# 03d7cec3-2701-40c5-a18e-b82317f9d7bb
# 8a1f4b98-fa1a-4c30-8132-aa285f5f0ec6
# 8a1f4b98-fa1a-4c30-8132-aa285f5f0ec6
# cdaca279-1cdf-452d-9ace-92bbcfecd4eb
# 1f6aa9f0-9614-4777-8a82-416fa3952050
# e8f99869-ebd4-4b8e-b8c6-a6e844fddb3c
# 204cef13-7d9d-4334-bc35-dbc561473f66
# 4e537381-fce2-4663-b670-ef19a2b60d85
# 50f2b2c3-e882-470f-ad7d-69f42a9919f8
# 805dcdd8-c804-4c05-8576-0a96e5963add
# df320af3-88bd-4a5e-a9a0-f01aeac71072


# проекты
# authors
# name
# classifier
# purl
# directDependencies
# uuid
# properties
# tags
# lastBomImport
# lastBomImportFormat
# lastInheritedRiskScore
# active
# isLatest
# metrics


# компоненты проекта
# authors
# name
# version
# classifier
# purl
# purlCoordinates
# description
# resolvedLicense
# externalReferences
# project
# lastInheritedRiskScore
# uuid
# author
# metrics
# repositoryMeta
# expandDependencyGraph
# isInternal


# components в уязвимостях проекта
# authors
# name
# version
# classifier
# purl
# purlCoordinates
# description
# resolvedLicense
# directDependencies
# externalReferences
# project
# lastInheritedRiskScore
# uuid
# expandDependencyGraph
# isInternal


# компонент из get_component_info
# authors
# name
# version
# classifier
# purl
# purlCoordinates
# description
# resolvedLicense
# directDependencies
# externalReferences
# project
# lastInheritedRiskScore
# uuid
# author
# expandDependencyGraph
# isInternal


# уязвимости компонента
# vulnId
# source
# description
# references
# published
# updated
# cvssV3BaseScore
# cvssV3ImpactSubScore
# cvssV3ExploitabilitySubScore
# cvssV3Vector
# severity
# epssScore
# epssPercentile
# uuid
# aliases
# affectedProjectCount
# affectedActiveProjectCount
# affectedInactiveProjectCount


# уязвимости проекта
# vulnId
# source
# description
# references
# published
# updated
# cvssV3BaseScore
# cvssV3ImpactSubScore
# cvssV3ExploitabilitySubScore
# cvssV3Vector
# severity
# epssScore
# epssPercentile
# components
# uuid
# aliases
# affectedProjectCount
# affectedActiveProjectCount
# affectedInactiveProjectCount


# def upload_sbom(project_name):
#     url = f"{DTRACK_URL}/api/v1/bom"

#     headers = {
#         'X-Api-Key': DTRACK_API_KEY
#     }

#     sbom_file_path = './services/dependencies/test_sbom.json'

#     with open(sbom_file_path, 'rb') as file:
#         print(file)
#         files = {
#             'bom': (sbom_file_path, file),
#             'project': (None, get_project_uuid(project_name))
#         }

#         response = requests.post(url, headers=headers, files=files)
#         if response.status_code == 200:
#             print("SBOM успешно импортирован")
#         else:
#             print(
#                 f"Ошибка при импорте SBOM: {response.status_code} - {response.text}")
#             print(response)
