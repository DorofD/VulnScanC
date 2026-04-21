from app.pg_repository.queries.projects import DBProjects


def add_project(name):
    DBProjects().add_project(name)


def get_projects():
    return (DBProjects().get_projects())


def delete_project(id):
    DBProjects().delete_project(id)


def change_project(id, name):
    DBProjects().update_project_name(id, name)
