import requests
import copy

from app.repository.queries.components import get_project_components
from app.repository.queries.licenses import get_component_licenses, add_license


class LicenseChecker:
    def __init__(self):
        self.sas = 1

    def check_github_license(self, component_url: str):
        """ В component_url ожидается ссылка на репозиторий в формате https://github.com/<owner>/<repo>"""

        result = {'status': 'error', 'license': '', 'error_description': ''}
        url = copy.deepcopy(component_url)
        if url.endswith(".git"):
            url = url[:-4]

        url_parts = url.split('/')

        try:
            owner = url_parts[-2]
            repo = url_parts[-1]
        except IndexError:
            result['status'] = 'error'
            result['error_description'] = f"Invalid url for GitHub repo: {component_url}"
            return result

        license_url = f"https://api.github.com/repos/{owner}/{repo}/license"

        response = requests.get(license_url)

        if response.status_code == 200:
            license_info = response.json()
            result['status'] = 'ok'
            result['license'] = license_info['license']
            return result
        elif response.status_code == 404:
            result['status'] = 'error'
            result['error_description'] = "404, license not found"
            return result
        else:
            result['status'] = 'error'
            result['error_description'] = "Unknown error"
            return result

    def check_gitlab_license(self, component_url: str):
        """
        Проверяет лицензию проекта на любом инстансе GitLab.
        :param component_url: URL репозитория (например, https://gitlab.gnome.org/GNOME/gdk-pixbuf.git)
        :return: Словарь с результатами проверки лицензии.
        """
        result = {'status': 'error', 'license': '', 'error_description': ''}
        url = copy.deepcopy(component_url)

        if url.endswith(".git"):
            url = url[:-4]

        url_parts = url.split('/')
        try:
            base_url = f"https://{url_parts[2]}"
            print(base_url)
            namespace = '/'.join(url_parts[3:-1])
            repo = url_parts[-1]
        except:
            result['status'] = 'error'
            result['error_description'] = f"Invalid URL for GitLab repo: {component_url}"
            return result

# https: // gitlab.gnome.org/api/v4/projects/33997?license = yes

        def search_project_id(project_name):
            projects = requests.get(
                f"{base_url}/api/v4/projects?search={project_name}")
            for project in projects.json():
                if project_name == project['name']:
                    return project['id']
            return False

        try:
            project_id = search_project_id(repo)
            assert project_id
        except:
            result['status'] = 'error'
            result['error_description'] = f"Project {repo} not found"
            return result

        project_with_license = f"{base_url}/api/v4/projects/{project_id}?license=yes"

        try:
            response = requests.get(project_with_license)
            if response.status_code == 200:
                if 'license' in response.json():
                    license_info = response.json()['license']
                result['status'] = 'ok'
                result['license'] = license_info
                return result
            elif response.status_code == 404:
                result['status'] = 'error'
                result['error_description'] = "404, license not found"
                return result
            else:
                result['status'] = 'error'
                result['error_description'] = f"Unknown error, status code: {response.status_code}"
                return result
        except requests.RequestException as e:
            result['status'] = 'error'
            result['error_description'] = f"Request failed: {str(e)}"
            return result

    def check_project_licenses(self, project_id):
        components = get_project_components(project_id)
        for component in components:
            component_licenses = get_component_licenses(component['id'])
            if 'github.com' in component['address']:
                license_check = self.check_github_license(component['address'])
                if license_check['status'] == 'ok':
                    add = 1
                    for existing_license in component_licenses:
                        if existing_license['name'] == license_check['license']['name']:
                            add = 0
                    if add:
                        add_license(component['id'], license_check['license']['key'],
                                    license_check['license']['name'], license_check['license']['key'], license_check['license']['url'])
                else:
                    continue
            if 'gitlab' in component['address']:
                license_check = self.check_gitlab_license(component['address'])
                if license_check['status'] == 'ok':
                    add = 1
                    for existing_license in component_licenses:
                        if existing_license['name'] == license_check['license']['name']:
                            add = 0
                    if add:
                        add_license(component['id'], license_check['license']['key'],
                                    license_check['license']['name'], license_check['license']['nickname'], license_check['license']['html_url'])
