from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBProjects():
    def __init__(self):
        pass

    def get_projects(self):
        query = "SELECT * FROM projects"
        return execute_query(query, fetch="all")

    def add_project(self, name: str, description: str = ''):
        query = """
            INSERT INTO projects (name, description)
            VALUES (%s, %s)
            RETURNING *
        """
        params = (name, description)
        return execute_query(query, params=params, fetch="one")

    def update_project(self, id: int, name: str = '', description: str = ''):
        query = "UPDATE projects SET "
        params = []

        if name:
            query += "name = %s, "
            params.append(name)

        if description:
            print("меняем описание")
            query += "description = %s, "
            params.append(description)

        query = query.rstrip(", ") + " WHERE id = %s RETURNING *"
        params.append(id)

        return execute_query(query, params=params, fetch="one")

    def delete_project(self, id: int):
        query = "DELETE FROM projects WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
