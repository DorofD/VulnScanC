from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBProjects:
    def __init__(self):
        pass

    def get_projects(self):
        query = "SELECT * FROM projects"
        return execute_query(query, fetch="all")

    def add_project(self, name: str):
        query = """
            INSERT INTO projects (name)
            VALUES (%s)
            RETURNING *
        """
        params = (name,)
        return execute_query(query, params=params, fetch="one")

    def update_project_name(self, id: int, name: str):
        query = """
            UPDATE projects
            SET name = %s
            WHERE id = %s
            RETURNING *
        """
        params = (name, id)
        return execute_query(query, params=params, fetch="one")

    def delete_project(self, id: int):
        query = "DELETE FROM projects WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
