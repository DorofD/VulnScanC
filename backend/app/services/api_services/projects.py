from app.pg_repository.queries.projects import DBProjects


def add_project(name, description):
    DBProjects().add_project(name, description)


def get_projects():
    return (DBProjects().get_projects())


def delete_project(id):
    DBProjects().delete_project(id)


def change_project(id, name, description):
    DBProjects().update_project(id, name, description)
