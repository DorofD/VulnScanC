from app.pg_repository.queries.base_query import execute_query

class DBBitbakeComponents():
    def __init__(self):
        pass

    def get_bitbake_component(self, id: int):
        query = "SELECT * FROM bitbake_components WHERE id = %s"
        return execute_query(query, params=(id,), fetch="one")

    def get_bitbake_components_with_licenses(self):
        query = "SELECT * FROM bitbake_components"
        components = execute_query(query, fetch="all")

        for component in components:
            query = "SELECT * FROM bitbake_licenses WHERE component_id = %s"
            component['licenses'] = execute_query(query, params=(component['id'],), fetch="all")

        return components

    def get_bitbake_components(self, project_id: int, layer: str):
        """Возвращает компоненты и кол-во уязвимостей для них"""
        query = """
            SELECT
                bc.*,
                COALESCE(vuln_counts.cve_count, 0) AS cve_count,
                COALESCE(bdu_counts.bdu_count, 0) AS bdu_count,
                COALESCE(license_counts.license_count, 0) AS license_count
            FROM bitbake_components AS bc
            LEFT JOIN (
                SELECT
                    component_id,
                    COUNT(*) AS cve_count
                FROM bitbake_vulnerabilities
                GROUP BY component_id
            ) AS vuln_counts
            ON bc.id = vuln_counts.component_id
            LEFT JOIN (
                SELECT
                    component_id,
                    COUNT(*) AS bdu_count
                FROM bdu_vulnerabilities
                WHERE component_type = 'bitbake'
                GROUP BY component_id
            ) AS bdu_counts
            ON bc.id = bdu_counts.component_id
            LEFT JOIN (
                SELECT
                    component_id,
                    COUNT(*) AS license_count
                FROM bitbake_licenses
                GROUP BY component_id
            ) AS license_counts
            ON bc.id = license_counts.component_id
            WHERE bc.project_id = %s AND bc.layer = %s;
        """
        return execute_query(query, params=(project_id, layer), fetch="all")

    def get_bitbake_project_components(self, project_id: int):
        """ Возвращает список компонентов по id проекта """
        query = """
            SELECT bitbake_components.*
            FROM bitbake_components
            JOIN bitbake_projects ON bitbake_components.project_id = bitbake_projects.id
            WHERE bitbake_projects.id = %s;
        """
        return execute_query(query, params=(project_id,), fetch="all")

    def add_bitbake_components(self, data_list: list):
        """в data_list ожидаемся список значений в формате [[project_id, name, version, layer], ...]"""
        query = """
            INSERT INTO bitbake_components (project_id, name, version, layer) 
            VALUES (%s, %s, %s, %s)
        """
        # execute_query handles multiple rows if data_list is a list of tuples/lists
        return execute_query(query, params=data_list)
