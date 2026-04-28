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
        # 1. Get project name
        query_project = """
            SELECT p.name
            FROM projects p
            JOIN snapshots s ON s.project_id = p.id
            WHERE s.id = %s
        """
        project_res = execute_query(query_project, params=(snapshot_id,), fetch="one")
        if not project_res:
            return None
        
        result = {'project_name': project_res['name']}

        # 2. Get snapshot details
        query_snapshot = "SELECT * FROM snapshots WHERE id = %s"
        snapshot = execute_query(query_snapshot, params=(snapshot_id,), fetch="one")
        result['datetime'] = snapshot['datetime']
        components_str = snapshot['components']

        # 3. Get components
        # Note: components_str is expected to be a comma-separated string of IDs like '1,2,3'
        # We need to convert it to a tuple for the IN clause
        component_ids = tuple(int(x.strip()) for x in components_str.split(',') if x.strip())
        
        if not component_ids:
            result['components'] = []
            return result

        query_components = "SELECT * FROM components WHERE id IN %s"
        components = execute_query(query_components, params=(component_ids,), fetch="all")

        # 4. Get vulnerabilities
        query_vulns = """
            SELECT v.*, c.id as component_id_ref
            FROM vulnerabilities v
            JOIN components c ON v.component_id = c.id
            WHERE c.id IN %s
        """
        vulnerabilities = execute_query(query_vulns, params=(component_ids,), fetch="all")

        # 5. Get BDU vulnerabilities
        query_bdu_vulns = """
            SELECT bv.*, c.id as component_id_ref
            FROM bdu_vulnerabilities bv
            JOIN components c ON bv.component_id = c.id
            WHERE c.id IN %s AND bv.component_type = 'common'
        """
        bdu_vulnerabilities = execute_query(query_bdu_vulns, params=(component_ids,), fetch="all")

        # 6. Get licenses
        query_licenses = "SELECT * FROM licenses WHERE component_id IN %s"
        licenses = execute_query(query_licenses, params=(component_ids,), fetch="all")

        # 7. Get comments
        query_comments = """
            SELECT cc.*, u.login AS user_name
            FROM components_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.component_id IN %s
        """
        comments = execute_query(query_comments, params=(component_ids,), fetch="all")

        # 8. Assemble components data
        for component in components:
            component['licenses'] = []
            component['comments'] = []
            component['vulnerabilities'] = []
            component['bdu_vulnerabilities'] = []
            
            comp_id = component['id']

            for vuln in vulnerabilities:
                if vuln['component_id'] == comp_id:
                    # The old code used vuln['full_data']. 
                    # Since we are using psycopg2, we'll assume the row itself is the data.
                    # If 'full_data' was a specific column, we should use that.
                    # Looking at the old code: component['vulnerabilities'].append(vuln['full_data'])
                    # I will check if 'full_data' exists, otherwise append the whole dict.
                    component['vulnerabilities'].append(vuln.get('full_data', vuln))

            for bdu_vuln in bdu_vulnerabilities:
                if bdu_vuln['component_id'] == comp_id:
                    component['bdu_vulnerabilities'].append(bdu_vuln)

            for lic in licenses:
                if lic['component_id'] == comp_id:
                    component['licenses'].append(lic)

            for comm in comments:
                if comm['component_id'] == comp_id:
                    component['comments'].append(comm)

        result['components'] = components
        return result
