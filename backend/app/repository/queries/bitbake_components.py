from app.repository.queries.base_query import execute_db_query


def get_bitbake_component(id: int):
    query = f"""
                SELECT * FROM bitbake_components WHERE id = '{id}';
            """
    return execute_db_query(query)


def get_bitbake_components_with_licenses():
    query = f"""
        SELECT * FROM bitbake_components;
    """
    components = execute_db_query(query)

    for component in components:
        query = f"""
            SELECT * FROM bitbake_licenses
            WHERE component_id = '{component['id']}';
        """
        component['licenses'] = execute_db_query(query)

    return components


def get_bitbake_components(project_id: int, layer: str):
    """Возвращает компоненты и кол-во уязвимостей для них"""
    # query = f"""
    #             SELECT * FROM bitbake_components
    #             WHERE id = '{project_id}' AND layer = '{layer}';
    #         """
    query = f"""
                SELECT
                    bc.*,
                    COUNT(bv.component_id) AS cve_count
                FROM bitbake_components AS bc
                LEFT JOIN bitbake_vulnerabilities AS bv
                    ON bc.id = bv.component_id
                WHERE bc.project_id = '{project_id}' AND bc.layer = '{layer}'
                GROUP BY bc.id;
            """
    query = f"""
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
        WHERE bc.project_id = '{project_id}' AND bc.layer = '{layer}';
    """

    return execute_db_query(query)


def get_bitbake_project_components(project_id: int):
    """ Возвращает список компонентов по id проекта """
    query = f"""
            SELECT bitbake_components.*
            FROM bitbake_components
            JOIN bitbake_projects ON bitbake_components.project_id = bitbake_projects.id
            WHERE bitbake_projects.id = '{project_id}';
            """
    return execute_db_query(query)


def add_bitbake_components(data_list: list):
    """в data_list ожидаемся список значений в формате [[project_id, name, version, layer], ...]"""
    query = f"""
            INSERT INTO bitbake_components ('project_id', 'name', 'version', 'layer') VALUES (?, ?, ?, ?);
            """
    return execute_db_query(query, data_list)
