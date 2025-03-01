from app.services.fstec.bdu_fstec import FSTEC
from app.repository.queries.vulnerabilities import get_vulnerabilities_ids
from app.repository.queries.bdu_vulnerabilities import add_bdu_vulnerabilities, get_bdu_vulnerabilities, get_bdu_vulnerabilities_count


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
                                bdu_vuln['status']
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
