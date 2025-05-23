import requests
import zipfile
import os
import xml.etree.ElementTree as ET
import time
from app.repository.queries.vulnerabilities import get_vulnerabilities_ids
from app.repository.queries.bitbake_vulnerabilities import get_bitbake_vulnerabilities_ids
from app.repository.queries.bdu_vulnerabilities import add_bdu_vulnerabilities, get_bdu_vulnerabilities, get_bdu_vulnerabilities_count, get_bdu_vulnerabilities_by_component


class FSTEC:
    def __init__(self):
        self.bdu_file = "./data/export.xml"

    def update_bdu(self):
        url = "https://bdu.fstec.ru/files/documents/vulxml.zip"
        archive_bdu = "./data/vulxml.zip"
        extract_path = self.bdu_file

        try:
            if os.path.exists(extract_path):
                os.remove(extract_path)
            if os.path.exists(archive_bdu):
                os.remove(archive_bdu)
            response = requests.get(url, stream=True, verify=False)

            if response.status_code == 200:
                with open(archive_bdu, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                with zipfile.ZipFile(archive_bdu, 'r') as zip_ref:
                    if "export/export.xml" in zip_ref.namelist():
                        with zip_ref.open("export/export.xml") as source_file:
                            with open(extract_path, "wb") as target_file:
                                target_file.write(source_file.read())
                    else:
                        raise Exception(
                            "export.xml not found in FSTEC BDU archive")
                os.remove(archive_bdu)
            else:
                raise Exception("Couldn't download FSTEC BDU")
        except Exception as e:
            raise Exception(e)

    def find_vulns_by_cve_id(self, cve_list, components_type):
        """в cve_list ожидается список словарей в формате [{'osv_id':id, component_id:'id'}]"""
        result = []
        if components_type == 'common':
            cve_text = 'osv_id'
        elif components_type == 'bitbake':
            cve_text = 'cve'
        else:
            raise Exception(f'Invalid components type: {components_type}')

        try:
            tree = ET.parse(self.bdu_file)
            root = tree.getroot()
            bdu_vulns = root.findall("vul")

            for vuln in bdu_vulns:
                try:
                    for identifier in vuln.find('identifiers').findall('identifier'):
                        if identifier.get('type') == "CVE":
                            for cve in cve_list:
                                if cve[cve_text] == identifier.text:
                                    try:
                                        try:
                                            bdu_severity = vuln.find(
                                                'severity').text
                                            if 'Критический' in bdu_severity:
                                                severity = "Critical"
                                            elif 'Высокий' in bdu_severity:
                                                severity = "High"
                                            elif 'Средний' in bdu_severity:
                                                severity = "Medium"
                                            elif 'Низкий' in bdu_severity:
                                                severity = "Low"
                                            else:
                                                severity = "not found"
                                        except:
                                            severity = 'not found'
                                            bdu_severity = "Не найдено"
                                        result.append({'component_id': cve['component_id'],
                                                       'component_type': components_type,
                                                       'bdu_id': vuln.find('identifier').text,
                                                       'cve_id': cve[cve_text],
                                                       'name': vuln.find('name').text,
                                                       'description': vuln.find('description').text,
                                                       'status': vuln.find('vul_status').text,
                                                       'bdu_severity': bdu_severity,
                                                       'severity': severity}
                                                      )
                                    except:
                                        raise Exception(
                                            f"Can't add founded vulnerability, check XML Parse for vulnerability with CVE ID: {cve[cve_text]}")
                # except IndentationError:
                #     # срабатывает, если в теге vul из БДУ нет вложенного тега identifiers
                #     pass
                except AttributeError:
                    # срабатывает, если в теге vul из БДУ нет вложенного тега identifiers
                    pass
            return result
        except FileNotFoundError:
            raise Exception("BDU file not found")
        except ET.ParseError as e:
            raise Exception("Error when parse BDU")

    def update_vulns(self, components_type):
        if components_type == 'common':
            vulns = get_vulnerabilities_ids()
        elif components_type == 'bitbake':
            vulns = get_bitbake_vulnerabilities_ids()
        else:
            raise Exception('Invalid components type')

        bdu_vulns = self.find_vulns_by_cve_id(vulns, components_type)
        vulns_to_add = []
        existing_bdu_vulns = get_bdu_vulnerabilities(components_type)

        for bdu_vuln in bdu_vulns:
            add = True
            for existing_bdu_vuln in existing_bdu_vulns:
                if bdu_vuln['component_id'] == existing_bdu_vuln['component_id'] and bdu_vuln['bdu_id'] == existing_bdu_vuln['bdu_id']:
                    add = False
            if add:
                vulns_to_add.append((bdu_vuln['component_id'],
                                    components_type,
                                    bdu_vuln['bdu_id'],
                                    bdu_vuln['cve_id'],
                                    bdu_vuln['name'],
                                    bdu_vuln['description'],
                                    bdu_vuln['status'],
                                    bdu_vuln['bdu_severity'],
                                    bdu_vuln['severity']
                                     ))
        if vulns_to_add:
            add_bdu_vulnerabilities(vulns_to_add)
        return True

    def get_component_bdu_vulns(self, component_id: int, component_type: str):
        vulns = get_bdu_vulnerabilities_by_component(
            component_id, component_type)

        critical_list = []
        high_list = []
        medium_list = []
        low_list = []
        not_found_list = []

        for vuln in vulns:
            if vuln['severity'] == 'not found':
                not_found_list.append(vuln)
                continue
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
        result = [*critical_list, *high_list, *
                  medium_list, *low_list, *not_found_list]
        return result

    def get_bdu_update_time(self):
        file_stats = os.stat(self.bdu_file)
        creation_time = file_stats.st_mtime
        readable_time = time.ctime(creation_time)
        return readable_time

    def get_bdu_info(self):
        result = {}
        result['last_update'] = self.get_bdu_update_time()
        result['vuln_count'] = get_bdu_vulnerabilities_count()
        return result
