from app.repository.queries.base_query import execute_db_query


def add_bitbake_snapshot(project_id: int, datetime: str, components: str):
    query = f"""
            INSERT INTO bitbake_snapshots ('project_id', 'datetime', 'components') VALUES('{project_id}', '{datetime}', '{components}');
            """
    return execute_db_query(query)


def get_bitbake_project_snapshots(project_id):
    query = f"""
        SELECT *
        FROM bitbake_snapshots
        WHERE project_id = {project_id};
        """
    return execute_db_query(query)


def get_bitbake_project_snapshots_with_components(project_id):
    query = f"""
        SELECT *
        FROM bitbake_snapshots
        WHERE project_id = {project_id};
        """
    return execute_db_query(query)


def delete_bitbake_snapshot(id):
    query = f"""
        DELETE FROM bitbake_snapshots
        WHERE id = '{id}'
        """
    return execute_db_query(query)


def get_all_bitbake_snapshot_data(id):
    # доработать для bitbake

    result = {}
    query = f"""
        SELECT bitbake_projects.name
        FROM bitbake_snapshots
        JOIN bitbake_projects ON bitbake_snapshots.project_id = bitbake_projects.id
        WHERE bitbake_snapshots.id = {id};
        """
    project_name = execute_db_query(query)[0]['name']
    result['project_name'] = project_name

    query = f"""
        SELECT *
        FROM bitbake_snapshots
        WHERE bitbake_snapshots.id = {id};
        """
    snapshot = execute_db_query(query)

    result['datetime'] = snapshot[0]['datetime']

    components_str = snapshot[0]['components']

    query = f"""
        SELECT * FROM bitbake_components WHERE id IN ({components_str});
    """

    components = execute_db_query(query)

    query = f"""
        SELECT *
        FROM bitbake_vulnerabilities
        JOIN bitbake_components ON bitbake_vulnerabilities.component_id = bitbake_components.id
        WHERE bitbake_components.id IN ({components_str});
    """

    vulnerabilities = execute_db_query(query)

    query = f"""
        SELECT *
        FROM bdu_vulnerabilities
        JOIN components ON bdu_vulnerabilities.component_id = components.id
        WHERE components.id IN ({components_str});
    """

    bdu_vulnerabilities = execute_db_query(query)

    query = f"""
        SELECT * FROM licenses;
    """

    licenses = execute_db_query(query)

    query = f"""
            SELECT cc.*, u.login AS user_name
            FROM components_comments cc
            JOIN users u ON cc.user_id = u.id
            """
    comments = execute_db_query(query)

    for component in components:
        component['licenses'] = []
        component['comments'] = []
        for vuln in vulnerabilities:
            if vuln['component_id'] == component['id']:
                if 'vulnerabilities' not in component:
                    component['vulnerabilities'] = []
                component['vulnerabilities'].append(vuln['full_data'])
        for vuln in bdu_vulnerabilities:
            if vuln['component_id'] == component['id']:
                if 'bdu_vulnerabilities' not in component:
                    component['bdu_vulnerabilities'] = []
                component['bdu_vulnerabilities'].append(vuln)
        for license in licenses:
            if license['component_id'] == component['id']:
                component['licenses'].append(license)
        for comment in comments:
            if comment['component_id'] == component['id']:
                component['comments'].append(comment)

    result['components'] = components
    return result
