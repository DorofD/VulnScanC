from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBComponents():
    def __init__(self):
        pass

    def get_project_components(self, project_id: int):
        query = """
            SELECT components.*
            FROM components
            JOIN projects ON components.project_id = projects.id
            WHERE projects.id = %s
        """
        return execute_query(query, params=(project_id,), fetch="all")

    def add_component(self, project_id: int, path: str, type: str = None, address: str = None, tag: str = None, version: str = None, score: float = None):
        query = """
            INSERT INTO components (project_id, path, type, address, tag, version, score, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'none')
            RETURNING *
        """
        params = (project_id, path, type, address, tag, version, score)
        try:
            return execute_query(query, params=params, fetch="one")
        except Exception:
            print(f"Error adding component: {params}")
            raise

    def get_component(self, component_id: int):
        query = "SELECT * FROM components WHERE id = %s"
        return execute_query(query, params=(component_id,), fetch="one")

    def change_component_status(self, component_id: int, new_status: str):
        query = "UPDATE components SET status = %s WHERE id = %s RETURNING *"
        params = (new_status, component_id)
        return execute_query(query, params=params, fetch="one")
