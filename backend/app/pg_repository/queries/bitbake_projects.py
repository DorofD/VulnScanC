from app.pg_repository.queries.base_query import execute_query

class DBBitbakeProjects():
    def __init__(self):
        pass

    def get_bitbake_projects(self):
        """Возвращает список в формате [{id: ..., 'name': ..., 'layers': ['layer1', 'layer2', ...]}, ...]"""
        query = "SELECT * FROM bitbake_projects"
        projects = execute_query(query, fetch="all")

        for project in projects:
            project['layers'] = []
            query = "SELECT DISTINCT layer FROM bitbake_components WHERE project_id = %s"
            layers = execute_query(query, params=(project['id'],), fetch="all")
            for layer in layers:
                project['layers'].append(layer['layer'])

        return projects

    def add_bitbake_project(self, name: str):
        query = "INSERT INTO bitbake_projects (name) VALUES (%s)"
        return execute_query(query, params=(name,))

    def get_bitbake_project(self, name: str):
        """ Возвращает проект по имени """
        query = "SELECT * FROM bitbake_projects WHERE name = %s"
        return execute_query(query, params=(name,), fetch="one")

    def update_bitbake_project(self, id: int, name: str):
        query = "UPDATE bitbake_projects SET name = %s WHERE id = %s"
        return execute_query(query, params=(name, id))

    def delete_bitbake_project(self, id: int):
        # The old implementation had cascading deletes manually. 
        # If the DB has foreign key constraints with ON DELETE CASCADE, 
        # we only need to delete the project. 
        # However, to be safe and match the old logic exactly:
        
        # 1. Delete vulnerabilities
        query_vuln = """
            DELETE FROM bitbake_vulnerabilities 
            WHERE component_id IN (
                SELECT id FROM bitbake_components WHERE project_id = %s
            )
        """
        execute_query(query_vuln, params=(id,))

        # 2. Delete components
        query_comp = "DELETE FROM bitbake_components WHERE project_id = %s"
        execute_query(query_comp, params=(id,))

        # 3. Delete snapshots
        query_snap = "DELETE FROM bitbake_snapshots WHERE project_id = %s"
        execute_query(query_snap, params=(id,))

        # 4. Delete project
        query_proj = "DELETE FROM bitbake_projects WHERE id = %s"
        return execute_query(query_proj, params=(id,))
