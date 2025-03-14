from app.services.fstec.bdu_fstec import FSTEC
from app.repository.queries.vulnerabilities import get_vulnerabilities_ids
from app.repository.queries.bdu_vulnerabilities import add_bdu_vulnerabilities, get_bdu_vulnerabilities, get_bdu_vulnerabilities_count, get_bdu_vulnerabilities_by_component


def update_bdu():
    fstec = FSTEC()
    fstec.update_bdu()
    return True


def update_vulns_by_cve_id():
    fstec = FSTEC()
    vulns = get_vulnerabilities_ids()
    bdu_vulns = fstec.find_vulns_by_cve_id(vulns)
    vulns_to_add = []
    existing_bdu_vulns = get_bdu_vulnerabilities()

    for bdu_vuln in bdu_vulns:
        add = True
        for existing_bdu_vuln in existing_bdu_vulns:
            if bdu_vuln['component_id'] == existing_bdu_vuln['component_id'] and bdu_vuln['bdu_id'] == existing_bdu_vuln['bdu_id']:
                add = False
        if add:
            vulns_to_add.append((bdu_vuln['component_id'],
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


def get_bdu_info():
    result = {}
    fstec = FSTEC()
    result['last_update'] = fstec.get_bdu_update_time()
    result['vuln_count'] = get_bdu_vulnerabilities_count()
    return result


def get_component_dbu_vulns(component_id: int):
    vulns = get_bdu_vulnerabilities_by_component(component_id)

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
