from app.pg_repository.queries.components import DBComponents
from app.pg_repository.queries.licenses import DBLicenses
from app.pg_repository.queries.vulnerabilities import DBVulnerabilities
from app.pg_repository.queries.bdu_vulnerabilities import DDBDUVulnerabilities


def get_project_components(id):
    db_components = DBComponents()
    db_licenses = DBLicenses()
    db_vulnerabilities = DBVulnerabilities()
    db_bdu_vulnerabilities = DDBDUVulnerabilities()

    components = db_components.get_project_components(id)

    for component in components:
        licenses = db_licenses.get_component_licenses(component['id'])
        osv_vuln_count = db_vulnerabilities.get_vulnerabilities_count_in_component(
            component['id'])
        bdu_vuln_coiunt = db_bdu_vulnerabilities.get_bdu_vulnerabilities_count_in_component(
            component['id'], component_type='common')

        component['licenses'] = licenses
        component['osv_vuln_count'] = osv_vuln_count
        component['bdu_vuln_count'] = bdu_vuln_coiunt
    return components


def change_component_status(id, status):
    """Возможные статусы: none, confirmed, denied"""
    db_components = DBComponents()
    db_components.change_component_status(id, status)
