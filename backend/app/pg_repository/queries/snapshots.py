from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query

class DBSnapshots():
    def __init__(self):
        pass

    def add_snapshot(self, project_id: int, datetime_str: str, components_str: str):
        query = """
            INSERT INTO snapshots (project_id, datetime, components)
            VALUES (%s, %s, %s)
            RETURNING *
        """
        params = (project_id, datetime_str, components_str)
        return execute_query(query, params=params, fetch="one")

    def get_project_snapshots(self, project_id: int):
        query = "SELECT * FROM snapshots WHERE project_id = %s"
        return execute_query(query, params=(project_id,), fetch="all")

    def get_project_snapshots_with_components(self, project_id: int):
        query = "SELECT * FROM snapshots WHERE project_id = %s"
        return execute_query(query, params=(project_id,), fetch="all")

    def delete_snapshot(self, snapshot_id: int):
        query = "DELETE FROM snapshots WHERE id = %s RETURNING *"
        return execute_query(query, params=(snapshot_id,), fetch="one")

    def get_all_snapshot_data(self, snapshot_id: int):
        # This method in the old repository was very complex and did many joins.
        # For the purpose of refactoring search_data.py, we only need the basic snapshot creation.
        # If search_data.py needed complex data, we would implement it here.
        # Currently, search_data.py only calls add_snapshot.
        pass
