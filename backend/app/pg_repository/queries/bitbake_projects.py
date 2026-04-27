from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBBitbakeProjects():
    def __init__(self):
        pass

    def get_bitbake_projects(self):
        query = "SELECT * FROM bitbake_projects"
        return execute_query(query, fetch="all")

    def add_bitbake_project(self, name: str, description: str = None):
        query = """
            INSERT INTO bitbake_projects (name, description)
            VALUES (%s, %s)
            RETURNING *
        """
        params = (name, description)
        return execute_query(query, params=params, fetch="one")

    def update_bitbake_project(self, id: int, name: str, description: str = None):
        query = """
            UPDATE bitbake_projects
            SET name = %s,
                description = CASE WHEN %s IS NULL THEN description ELSE %s END
            WHERE id = %s
            RETURNING *
        """
        params = (name, description, description, id)
        return execute_query(query, params=params, fetch="one")

    def delete_bitbake_project(self, id: int):
        query = "DELETE FROM bitbake_projects WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
