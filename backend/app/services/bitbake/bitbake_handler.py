from datetime import datetime

from app.repository.queries.bitbake_projects import add_bitbake_project, get_bitbake_project, get_bitbake_projects, delete_bitbake_project
from app.repository.queries.bitbake_components import add_bitbake_components, get_bitbake_component, get_bitbake_project_components
from app.repository.queries.bitbake_vulnerabilities import get_bitbake_vulnerabilities_by_component, get_bitbake_vulnerabilities_by_components
from app.repository.queries.bitbake_vulnerabilities import get_bitbake_vulnerabilities_count_in_component, get_bitbake_vulnerabilities_ids, add_bitbake_vulnerabilities
from app.repository.queries.bitbake_snapshots import add_bitbake_snapshot


class BitbakeHandler:
    def __init__(self):
        pass

    def parse_cve_report(self, cve_report):
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
