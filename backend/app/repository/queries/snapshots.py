from app.repository.queries.base_query import execute_db_query


def add_snapshot(project_id: int, datetime: str, components: str):
    query = f"""
            INSERT INTO snapshots ('project_id', 'datetime', 'components') VALUES('{project_id}', '{datetime}', '{components}');
            """
    return execute_db_query(query)


def get_project_snapshots(project_id):
    query = f"""
        SELECT *
        FROM snapshots
        WHERE project_id = {project_id};
        """
    return execute_db_query(query)


def get_project_snapshots_with_components(project_id):
    query = f"""
        SELECT *
        FROM snapshots
        WHERE project_id = {project_id};
        """
    return execute_db_query(query)


def delete_snapshot(id):
    query = f"""
        DELETE FROM snapshots
        WHERE id = '{id}'
        """
    return execute_db_query(query)


def get_all_snapshot_data(id):

    result = {}
    query = f"""
        SELECT projects.name
        FROM snapshots
        JOIN projects ON snapshots.project_id = projects.id
        WHERE snapshots.id = {id};
        """
    project_name = execute_db_query(query)[0]['name']
    result['project_name'] = project_name

    query = f"""
        SELECT *
        FROM snapshots
        WHERE snapshots.id = {id};
        """
    snapshot = execute_db_query(query)

    result['datetime'] = snapshot[0]['datetime']

    components_str = snapshot[0]['components']

    query = f"""
        SELECT * FROM components WHERE id IN ({components_str});
    """

    components = execute_db_query(query)

    query = f"""
        SELECT *
        FROM vulnerabilities
        JOIN components ON vulnerabilities.component_id = components.id
        WHERE components.id IN ({components_str});
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
