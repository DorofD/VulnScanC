from app.repository.queries.components import get_project_components as get_project_components_db
from app.repository.queries.components import change_component_status as change_component_status_db
from app.repository.queries.licenses import get_component_licenses as get_component_licenses_db


def get_project_components(id):
    components = get_project_components_db(id)
    for component in components:
        licenses = get_component_licenses_db(component['id'])
        component['licenses'] = licenses
    return components


def change_component_status(id, status):
    """Возможные статусы: none, confirmed, denied"""
    change_component_status_db(id, status)
