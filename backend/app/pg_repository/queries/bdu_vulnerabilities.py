from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query

class DDBDUVulnerabilities():
    def __init__(self):
        pass

    def get_bdu_vulnerabilities(self, component_type: str):
        query = "SELECT * FROM bdu_vulnerabilities WHERE component_type = %s"
        return execute_query(query, params=(component_type,), fetch="all")

    def get_bdu_vulnerabilities_by_components(self, id_list: list, component_type: str):
        if not id_list:
            return []
        query = "SELECT * FROM bdu_vulnerabilities WHERE component_id IN %s AND component_type = %s"
        return execute_query(query, params=(tuple(id_list), component_type), fetch="all")

    def get_bdu_vulnerabilities_by_component(self, component_id: int, component_type: str):
        query = "SELECT * FROM bdu_vulnerabilities WHERE component_id = %s AND component_type = %s"
        return execute_query(query, params=(component_id, component_type), fetch="one")

    def get_bdu_vulnerabilities_count(self):
        query = "SELECT COUNT(*) as count FROM bdu_vulnerabilities"
        res = execute_query(query, fetch="one")
        return res['count'] if res else 0

    def get_bdu_vulnerabilities_count_in_component(self, component_id: int, component_type: str):
        query = "SELECT COUNT(*) as count FROM bdu_vulnerabilities WHERE component_id = %s AND component_type = %s"
        res = execute_query(query, params=(component_id, component_type), fetch="one")
        return res['count'] if res else 0

    def add_bdu_vulnerabilities(self, data_list: list):
        """
        data_list is expected to be a list of dictionaries:
        [{'component_id': ..., 'component_type': ..., 'bdu_id': ..., 'cve_id': ..., 'name': ..., 'description': ..., 'status': ..., 'bdu_severity': ..., 'severity': ...}]
        """
        if not data_list:
            return

        # Since execute_query uses cur.execute(query, params), 
        # and cur.execute(query, list_of_dicts) is NOT standard for executemany,
        # we should implement a loop or use a more robust way if execute_query doesn't support it.
        # However, to keep it simple and consistent with the current execute_query:
        
        query = """
            INSERT INTO bdu_vulnerabilities (component_id, component_type, bdu_id, cve_id, name, description, status, bdu_severity, severity)
            VALUES (%(component_id)s, %(component_type)s, %(bdu_id)s, %(cve_id)s, %(name)s, %(description)s, %(status)s, %(bdu_severity)s, %(severity)s)
        """
        
        # We'll manually iterate to ensure compatibility with the current execute_query implementation
        # which only calls cur.execute once.
        import psycopg2
        import os
        from dotenv import load_dotenv
        load_dotenv('.env')
        DB_CONFIG = {
            'host': os.environ['POSTGRES_HOST'],
            'port': os.environ['POSTGRES_PORT'],
            'database': os.environ['POSTGRES_DB'],
            'user': os.environ['POSTGRES_USER'],
            'password': os.environ['POSTGRES_PASSWORD']
        }
        
        conn = psycopg2.connect(**DB_CONFIG)
        try:
            with conn, conn.cursor() as cur:
                for item in data_list:
                    cur.execute(query, item)
        finally:
            conn.close()
