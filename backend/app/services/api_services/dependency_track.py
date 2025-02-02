from app.services.dependency_track.api import DT


def get_projects():
    dt = DT()
    return dt.get_projects()


def get_components(project_uuid):
    dt = DT()
    return dt.get_vulnerable_project_components(project_uuid)
