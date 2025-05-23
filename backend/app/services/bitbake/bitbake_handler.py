from datetime import datetime

from app.repository.queries.bitbake_projects import add_bitbake_project, get_bitbake_project, get_bitbake_projects, delete_bitbake_project, change_bitbake_project
from app.repository.queries.bitbake_components import add_bitbake_components, get_bitbake_components, get_bitbake_project_components, get_bitbake_components_with_licenses
from app.repository.queries.bitbake_vulnerabilities import get_bitbake_vulnerabilities_by_component, get_bitbake_vulnerabilities_by_components
from app.repository.queries.bitbake_vulnerabilities import get_bitbake_vulnerabilities_count_in_component, get_bitbake_vulnerabilities_ids, add_bitbake_vulnerabilities
from app.repository.queries.bitbake_snapshots import add_bitbake_snapshot
from app.repository.queries.bitbake_licenses import add_bitbake_license, get_bitbake_component_licenses, delete_bitbake_license


class BitbakeHandler:
    def __init__(self):
        pass

    def add_project(self, project_name):
        add_bitbake_project(project_name)
        return True

    def add_license(self, component_id, license_name, recipe_name):
        add_bitbake_license(component_id, license_name, recipe_name)
        return True

    def delete_project(self, project_id):
        delete_bitbake_project(project_id)
        return True

    def delete_license(self, license_id):
        delete_bitbake_license(license_id)
        return True

    def change_project(self, project_id, new_project_name):
        change_bitbake_project(project_id, new_project_name)
        return True

    def get_projects(self):
        return get_bitbake_projects()

    def get_components(self, project_id, layer):
        components = get_bitbake_components(project_id, layer)
        for component in components:
            licenses = get_bitbake_component_licenses(component['id'])
            component['licenses'] = licenses
        return components

    def get_vulnerabilities(self, component_id):
        vulns = get_bitbake_vulnerabilities_by_component(component_id)
        critical_list = []
        high_list = []
        medium_list = []
        low_list = []
        none_list = []
        unknown_list = []
        for vuln in vulns:
            if vuln['severity'] == 'Critical':
                critical_list.append(vuln)
                continue
            if vuln['severity'] == 'High':
                high_list.append(vuln)
                continue
            if vuln['severity'] == 'Medium':
                medium_list.append(vuln)
                continue
            if vuln['severity'] == 'Low':
                low_list.append(vuln)
                continue
            if vuln['severity'] == 'None':
                none_list.append(vuln)
                continue
            if vuln['severity'] == 'Unknown':
                unknown_list.append(vuln)
                continue
        result = [*critical_list, *high_list, *medium_list,
                  *low_list, *none_list, *unknown_list]
        return result

    def parse_cve_report(self, cve_report):
        """
        Парсит bitbake отчёт формата .cve, возвращает объект:
        {'layers':
          'layer_name':
            'package_name':
              'version': ...,
              'cves':
                'some_cve':
                  'cve_status': ...,
                  'cve_summary': ...,
                  'cvss_v2': ...,
                  'cvss_v3': ...,
                  'vector': ...,
                  'more_information': ...}
        """
        content = cve_report.read().decode('utf-8')
        # with open(content, "r", encoding='utf-8') as file:
        lines = content.splitlines()
        initial_lines = {
            'layer': "LAYER: ",
            'package_name': "PACKAGE NAME: ",
            'package_version': "PACKAGE VERSION: ",
            'cve': "CVE: ",
            'cve_status': "CVE STATUS: ",
            'cve_summary': "CVE SUMMARY: ",
            'cvss_v2': "CVSS v2 BASE SCORE: ",
            'cvss_v3': "CVSS v3 BASE SCORE: ",
            'vector': "VECTOR: ",
            'more_information': "MORE INFORMATION: "
        }

        parsed_result = {"layers": {}}
        current_layer = ''
        current_package = ''
        cve_summary_adding = False
        more_information_adding = False
        for line in lines:

            if initial_lines["layer"] in line:
                cve_summary_adding = False
                if more_information_adding:
                    parsed_result['layers'][current_layer][current_package][
                        'cves'][current_cve]['more_information'] = more_information
                    more_information_adding = False

                current_layer = line.replace(
                    initial_lines["layer"], '')
                current_layer = current_layer.replace('\n', '')
                if current_layer not in parsed_result['layers']:
                    parsed_result['layers'][current_layer] = {}

            if initial_lines["package_name"] in line:
                current_package = line.replace(
                    initial_lines["package_name"], '')
                current_package = current_package.replace('\n', '')
                if current_package not in parsed_result['layers'][current_layer]:
                    parsed_result['layers'][current_layer][current_package] = {
                        'version': '', 'cves': {}}

            if initial_lines["package_version"] in line:
                package_version = line.replace(
                    initial_lines["package_version"], '')
                package_version = package_version.replace('\n', '')
                parsed_result['layers'][current_layer][current_package]['version'] = package_version

            if initial_lines["cve"] in line:
                current_cve = line.replace(initial_lines["cve"], '')
                current_cve = current_cve.replace('\n', '')
                if current_cve not in parsed_result['layers'][current_layer][current_package]['cves']:
                    parsed_result['layers'][current_layer][current_package]['cves'][current_cve] = {
                        'cve_status': "",
                        'cve_summary': "",
                        'cvss_v2': "",
                        'cvss_v3': "",
                        'severity': "",
                        'vector': "",
                        'more_information': ""
                    }

            if initial_lines["cve_status"] in line:
                cve_status = line.replace(
                    initial_lines["cve_status"], '')
                cve_status = cve_status.replace('\n', '')
                parsed_result['layers'][current_layer][current_package]['cves'][current_cve]['cve_status'] = cve_status

            if initial_lines["cve_summary"] in line or cve_summary_adding:
                if not cve_summary_adding:
                    cve_summary_adding = True
                    cve_summary = line.replace(
                        initial_lines["cve_summary"], '')
                    continue
                else:
                    if initial_lines["cvss_v2"] in line or initial_lines["cvss_v3"] in line or initial_lines["vector"] in line or initial_lines["more_information"] in line:
                        parsed_result['layers'][current_layer][current_package]['cves'][current_cve]['cve_summary'] = cve_summary
                        cve_summary_adding = False
                    else:
                        cve_summary += line
                        cve_summary += '\n'
                        continue

            if initial_lines["cvss_v2"] in line:
                cvss_v2 = line.replace(initial_lines["cvss_v2"], '')
                cvss_v2 = cvss_v2.replace('\n', '')
                parsed_result['layers'][current_layer][current_package]['cves'][current_cve]['cvss_v2'] = cvss_v2

            if initial_lines["cvss_v3"] in line:
                cvss_v3 = line.replace(initial_lines["cvss_v3"], '')
                cvss_v3 = cvss_v3.replace('\n', '')
                parsed_result['layers'][current_layer][current_package]['cves'][current_cve]['cvss_v3'] = cvss_v3
                float_cvss = float(cvss_v3)
                severity = 'Unknown'
                if float_cvss == 0:
                    severity = "None"
                elif 0.1 <= float_cvss <= 3.9:
                    severity = "Low"
                elif 4.0 <= float_cvss <= 6.9:
                    severity = "Medium"
                elif 7.0 <= float_cvss <= 8.9:
                    severity = "High"
                elif 9.0 <= float_cvss <= 10.0:
                    severity = "Critical"
                parsed_result['layers'][current_layer][current_package]['cves'][current_cve]['severity'] = severity

            if initial_lines["vector"] in line:
                vector = line.replace(initial_lines["vector"], '')
                vector = vector.replace('\n', '')
                parsed_result['layers'][current_layer][current_package]['cves'][current_cve]['vector'] = vector

            if initial_lines["more_information"] in line or more_information_adding:
                if not more_information_adding:
                    more_information_adding = True
                    more_information = line.replace(
                        initial_lines["more_information"], '')
                    continue
                else:
                    if line != '\n':
                        more_information += line
                        more_information += '\n'
                    continue
        return parsed_result

    def save_report_results(self, project_name, report_results):
        try:
            project = get_bitbake_project(project_name)[0]
        except IndexError:
            raise Exception(f"Don't found project {project_name}")

        existing_components = get_bitbake_project_components(project['id'])

        components_to_add = []
        for layer in report_results['layers']:
            for component in report_results['layers'][layer]:
                add = True
                for existing_component in existing_components:
                    if component == existing_component['name'] and report_results['layers'][layer][component]['version'] == existing_component['version']:
                        add = False
                if add:
                    components_to_add.append(
                        [project['id'], component, report_results['layers'][layer][component]['version'], layer])
        if components_to_add:
            add_bitbake_components(components_to_add)

        existing_components = get_bitbake_project_components(project['id'])

        report_components_list = {}
        for layer in report_results['layers']:
            for component in report_results['layers'][layer]:
                report_components_list[component] = report_results['layers'][layer][component]

        vulnerabilities_to_add = []
        for existing_component in existing_components:
            for report_component in report_components_list:
                if report_component == existing_component['name'] and report_components_list[report_component]['version'] == existing_component['version']:
                    existing_vulnerabilities = get_bitbake_vulnerabilities_by_component(
                        existing_component['id'])
                    for report_vuln in report_components_list[report_component]['cves']:
                        add = True
                        for existing_vuln in existing_vulnerabilities:
                            if report_vuln == existing_vuln['cve']:
                                add = False
                        if add:
                            vulnerabilities_to_add.append([existing_component['id'],
                                                           report_vuln,
                                                           report_components_list[report_component][
                                                               'cves'][report_vuln]['cve_status'],
                                                           report_components_list[report_component][
                                                               'cves'][report_vuln]['cve_summary'],
                                                           report_components_list[report_component]['cves'][report_vuln]['cvss_v2'],
                                                           report_components_list[report_component]['cves'][report_vuln]['cvss_v3'],
                                                           report_components_list[report_component][
                                                               'cves'][report_vuln]['severity'],
                                                           report_components_list[report_component]['cves'][report_vuln]['vector'],
                                                           report_components_list[report_component][
                                                               'cves'][report_vuln]['more_information'],
                                                           ])
        if vulnerabilities_to_add:
            add_bitbake_vulnerabilities(vulnerabilities_to_add)

        # создание снапшота
        try:
            now = datetime.now()
            datetime_str = now.strftime("%d.%m.%Y %H:%M")
            existing_components = get_bitbake_project_components(project['id'])
            existing_components_name_id_dict = {
                component['name']: component['id'] for component in existing_components}
            components_ids_snapshot = []
            for component in report_components_list:
                components_ids_snapshot.append(
                    existing_components_name_id_dict[component])
            components_ids_snapshot_str = ', '.join(
                map(str, components_ids_snapshot))
            add_bitbake_snapshot(
                project['id'], datetime_str, components_ids_snapshot_str)
        except Exception as exc:
            raise Exception(f"Error when create snapshot: {exc}")
        return True

    def parse_licenses(self, license_file):
        """
        Парсит bitbake отчёт формата license.manifest, возвращает объект:
        [{package_name: .., package_version: .., recipe_name: .., licenses: ['license1', 'license2', ..]}, ..]
        """
        content = license_file.read().decode('utf-8')
        lines = content.splitlines()

        initial_lines = {
            'package_name': "PACKAGE NAME: ",
            'package_version': "PACKAGE VERSION: ",
            'recipe_name': "RECIPE NAME: ",
            'license': "LICENSE: "
        }

        parsed_result = []
        current_package = {}

        for line in lines:
            if initial_lines['package_name'] in line:
                if current_package:
                    parsed_result.append(current_package)
                current_package = {
                    'package_name': line.replace(initial_lines['package_name'], '').strip()
                }

            elif initial_lines['package_version'] in line:
                current_package['package_version'] = line.replace(
                    initial_lines['package_version'], '').strip()

            elif initial_lines['recipe_name'] in line:
                current_package['recipe_name'] = line.replace(
                    initial_lines['recipe_name'], '').strip()

            elif initial_lines['license'] in line:
                license_line = line.replace(
                    initial_lines['license'], '').strip()
                if '&' in license_line:
                    current_package['licenses'] = license_line.replace(
                        " ", "").split("&")
                elif '|' in license_line:
                    current_package['licenses'] = license_line.replace(
                        " ", "").split("|")
                else:
                    current_package['licenses'] = [license_line]

        if current_package:
            parsed_result.append(current_package)
        return parsed_result

    def update_licenses(self, parsed_licenses):
        components = get_bitbake_components_with_licenses()
        licenses_to_add = []
        for component in components:
            for note in parsed_licenses:
                if note['package_name'] == component['name'] and note['package_version'] == component['version']:
                    existing_licenses = {license['license']
                                         for license in component['licenses']}
                    for license in note['licenses']:
                        if license not in existing_licenses:
                            licenses_to_add.append(
                                {'component_id': component['id'], 'license': license, 'recipe_name': note['recipe_name']})
        for license in licenses_to_add:
            add_bitbake_license(
                license['component_id'], license['license'], license['recipe_name'])
