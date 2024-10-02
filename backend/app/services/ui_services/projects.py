from app.repository.queries.projects import add_project as add_project_db
from app.repository.queries.projects import get_project as get_project_db
from app.repository.queries.projects import get_projects as get_projects_db
from app.repository.queries.projects import delete_project as delete_project_db
from app.repository.queries.projects import change_project as change_project_db


def add_project(name):
    add_project_db(name)


def get_project(name):
    return (get_project_db(name))


def get_projects():
    return (get_projects_db())


def delete_project(id):
    delete_project_db(id)


def change_project(id, name):
    change_project_db(id, name)
