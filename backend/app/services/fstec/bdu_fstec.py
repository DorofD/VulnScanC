import requests
import zipfile
import os
import xml.etree.ElementTree as ET
import time


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

    def find_vulns_by_cve_id(self, cve_list):
        """в cve_list ожидается список словарей в формате [{'osv_id':id, component_id:'id'}]"""
        result = []
        try:
            tree = ET.parse(self.bdu_file)
            root = tree.getroot()
            bdu_vulns = root.findall("vul")

            for vuln in bdu_vulns:
                try:
                    for identifier in vuln.find('identifiers').findall('identifier'):
                        if identifier.get('type') == "CVE":
                            for cve in cve_list:
                                if cve['osv_id'] == identifier.text:
                                    try:
                                        result.append({'component_id': cve['component_id'],
                                                       'bdu_id': vuln.find('identifier').text,
                                                       'cve_id': cve['osv_id'],
                                                       'name': vuln.find('name').text,
                                                       'description': vuln.find('description').text,
                                                       'status': vuln.find('vul_status').text})
                                    except:
                                        raise Exception(
                                            f"Can't add founded vulnerability, check XML Parse for vulnerability with CVE ID: {cve['osv_id']}")
                # except IndentationError:
                #     # срабатывает, если в теге vul из БДУ нет вложенного тега identifiers
                #     pass
                except AttributeError:
                    # срабатывает, если в теге vul из БДУ нет вложенного тега identifiers
                    pass
            return result
        except FileNotFoundError:
            print(f"BDU not found")
        except ET.ParseError as e:
            print(f"Error when parse BDU")

    def get_bdu_update_time(self):
        file_stats = os.stat(self.bdu_file)
        creation_time = file_stats.st_mtime
        readable_time = time.ctime(creation_time)
        return readable_time
