from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query

class DBLicenses():
    def __init__(self):
        pass

    def add_license(self, component_id: int, key: str, name: str, spdx_id: str, url: str):
        query = """
            INSERT INTO licenses (component_id, key, name, spdx_id, url)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """
        params = (component_id, key, name, spdx_id, url)
        return execute_query(query, params=params, fetch="one")

    def get_component_licenses(self, component_id: int):
        query = "SELECT * FROM licenses WHERE component_id = %s"
        return execute_query(query, params=(component_id,), fetch="all")

    def delete_license(self, license_id: int):
        query = "DELETE FROM licenses WHERE id = %s RETURNING *"
        return execute_query(query, params=(license_id,), fetch="one")
