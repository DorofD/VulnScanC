from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query

class DBVulnerabilities():
    def __init__(self):
        pass

    def get_vulnerabilities_by_components(self, component_ids: list):
        query = "SELECT * FROM vulnerabilities WHERE component_id IN %s"
        # execute_query with IN clause usually expects a tuple
        params = (tuple(component_ids),)
        return execute_query(query, params=params, fetch="all")

    def get_vulnerabilities_by_component(self, component_id: int):
        query = "SELECT * FROM vulnerabilities WHERE component_id = %s"
        return execute_query(query, params=(component_id,), fetch="one")

    def get_vulnerabilities_count_in_component(self, component_id: int):
        query = "SELECT COUNT(*) FROM vulnerabilities WHERE component_id = %s"
        result = execute_query(query, params=(component_id,), fetch="one")
        # Depending on how execute_query returns, we might need to access it differently
        # Based on previous patterns, it returns a list of dicts
        return result[0]['count'] if result and 'count' in result[0] else result[0]['COUNT(*)']

    def add_vulnerabilities(self, data_list: list):
        """
        data_list: list of tuples (component_id, osv_id, full_data)
        """
        query = """
            INSERT INTO vulnerabilities (component_id, osv_id, full_data)
            VALUES %s
        """
        # Using execute_values style or multiple inserts
        # Since execute_query is a wrapper, let's assume it handles multiple inserts or we loop
        # However, a more standard way for psycopg2 is execute_values.
        # If execute_query is simple, we'll loop.
        for item in data_list:
            # item is (component_id, osv_id, full_data)
            q = "INSERT INTO vulnerabilities (component_id, osv_id, full_data) VALUES (%s, %s, %s)"
            execute_query(q, params=item, fetch="one")
