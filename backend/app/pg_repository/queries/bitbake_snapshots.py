from app.pg_repository.queries.base_query import execute_query

class DBBitbakeSnapshots():
    def __init__(self):
        pass

    def add_bitbake_snapshot(self, project_id: int, datetime_str: str, components_str: str):
        query = """
            INSERT INTO bitbake_snapshots (project_id, datetime, components)
            VALUES (%s, %s, %s)
        """
        return execute_query(query, params=(project_id, datetime_str, components_str))

    def get_bitbake_project_snapshots(self, project_id: int):
        query = "SELECT * FROM bitbake_snapshots WHERE project_id = %s"
        return execute_query(query, params=(project_id,), fetch="all")

    def get_bitbake_project_snapshots_with_components(self, project_id: int):
        # In the old implementation, this was identical to get_bitbake_project_snapshots
        return self.get_bitbake_project_snapshots(project_id)

    def delete_bitbake_snapshot(self, snapshot_id: int):
        query = "DELETE FROM bitbake_snapshots WHERE id = %s"
        return execute_query(query, params=(snapshot_id,))

    def get_all_bitbake_snapshot_data(self, snapshot_id: int):
        """
        Complex method to reconstruct the full snapshot state.
        Replicates the logic from the old repository layer.
        """
        # 1. Get snapshot and project name
        query_snap = """
            SELECT s.datetime, s.components, p.name as project_name
            FROM bitbake_snapshots s
            JOIN bitbake_projects p ON s.project_id = p.id
            WHERE s.id = %s
        """
        snapshot_row = execute_query(query_snap, params=(snapshot_id,), fetch="one")
        if not snapshot_row:
            return None

        result = {
            'project_name': snapshot_row['project_name'],
            'datetime': snapshot_row['datetime'],
            'components': {},
            'layers': []
        }

        components_ids_str = snapshot_row['components']
        # components_ids_str is expected to be a comma-separated string of IDs like '1,2,3'
        # We convert it to a tuple for the IN clause
        component_ids = tuple(int(x.strip()) for x in components_ids_str.split(',') if x.strip())

        if not component_ids:
            return result

        # 2. Get components
        query_comp = "SELECT * FROM bitbake_components WHERE id IN %s"
        components = execute_query(query_comp, params=(component_ids,), fetch="all")

        # 3. Get vulnerabilities (Unpatched)
        query_vuln = """
            SELECT bv.*, bc.name as component_name
            FROM bitbake_vulnerabilities bv
            JOIN bitbake_components bc ON bv.component_id = bc.id
            WHERE bc.id IN %s AND bv.status = 'Unpatched'
        """
        vulnerabilities = execute_query(query_vuln, params=(component_ids,), fetch="all")

        # 4. Get BDU vulnerabilities
        query_bdu = """
            SELECT bdu.*, bc.name as component_name
            FROM bdu_vulnerabilities bdu
            JOIN bitbake_components bc ON bdu.component_id = bc.id
            WHERE bc.id IN %s AND bdu.component_type = 'bitbake'
        """
        bdu_vulnerabilities = execute_query(query_bdu, params=(component_ids,), fetch="all")

        # 5. Get licenses
        query_lic = "SELECT * FROM bitbake_licenses WHERE component_id IN %s"
        licenses = execute_query(query_lic, params=(component_ids,), fetch="all")

        # 6. Get component comments
        query_comp_comm = """
            SELECT cc.*, u.login AS user_name
            FROM bitbake_components_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.component_id IN %s
        """
        components_comments = execute_query(query_comp_comm, params=(component_ids,), fetch="all")

        # 7. Get vulnerability comments
        # We need to find which vulnerability comments belong to the vulnerabilities we fetched
        vuln_ids = tuple(v['id'] for v in vulnerabilities)
        vulns_comments = []
        if vuln_ids:
            query_vuln_comm = """
                SELECT cc.*, u.login AS user_name
                FROM bitbake_vulnerabilities_comments cc
                JOIN users u ON cc.user_id = u.id
                WHERE cc.vuln_id IN %s
            """
            vulns_comments = execute_query(query_vuln_comm, params=(vuln_ids,), fetch="all")

        # 8. Assemble the data structure
        for component in components:
            comp_id = component['id']
            component['licenses'] = [l for l in licenses if l['component_id'] == comp_id]
            component['comments'] = [c for c in components_comments if c['component_id'] == comp_id]
            
            # Vulnerabilities
            comp_vulns = []
            for v in vulnerabilities:
                if v['component_id'] == comp_id:
                    v_copy = v.copy()
                    v_copy['comments'] = [vc for vc in vulns_comments if vc['vuln_id'] == v['id']]
                    comp_vulns.append(v_copy)
            component['vulnerabilities'] = comp_vulns

            # BDU Vulnerabilities
            component['bdu_vulnerabilities'] = [b for b in bdu_vulnerabilities if b['component_id'] == comp_id]

            # Organize by layer
            layer = component['layer']
            if layer not in result['layers']:
                result['layers'].append(layer)
                result['components'][layer] = []
            result['components'][layer].append(component)

        return result
