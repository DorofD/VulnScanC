from app.repository.queries.components import get_project_components as get_project_components_db
from app.repository.queries.components import change_component_status as change_component_status_db


def get_project_components(id):
    return get_project_components_db(id)


def change_component_status(id, status):
    """Возможные статусы: none, confirmed, denied"""
    change_component_status_db(id, status)
