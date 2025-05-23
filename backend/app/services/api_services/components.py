from app.repository.queries.components import get_project_components as get_project_components_db
from app.repository.queries.components import change_component_status as change_component_status_db
from app.repository.queries.licenses import get_component_licenses as get_component_licenses_db
from app.repository.queries.vulnerabilities import get_vulnerabilities_count_in_component
from app.repository.queries.bdu_vulnerabilities import get_bdu_vulnerabilities_count_in_component


def get_project_components(id):
    components = get_project_components_db(id)

    for component in components:
        licenses = get_component_licenses_db(component['id'])
        osv_vuln_count = get_vulnerabilities_count_in_component(
            component['id'])
        bdu_vuln_coiunt = get_bdu_vulnerabilities_count_in_component(
            component['id'], component_type='common')

        component['licenses'] = licenses
        component['osv_vuln_count'] = osv_vuln_count
        component['bdu_vuln_count'] = bdu_vuln_coiunt
    return components


def change_component_status(id, status):
    """Возможные статусы: none, confirmed, denied"""
    change_component_status_db(id, status)
