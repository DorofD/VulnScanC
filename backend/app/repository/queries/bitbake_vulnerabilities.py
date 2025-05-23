from app.repository.queries.base_query import execute_db_query


def get_bitbake_vulnerabilities_ids():
    """ Возвращает cve и component_id уязвимостей со статусом Unpatched"""
    query = f"""
        SELECT cve, component_id
        FROM bitbake_vulnerabilities
        WHERE status = 'Unpatched';
        """
    return execute_db_query(query)


def get_bitbake_vulnerabilities_by_components(id_list: list):
    """ Возвращает список уязвимостей в компонентах """
    ids = ', '.join(map(str, id_list))
    query = f"""
        SELECT *
        FROM bitbake_vulnerabilities
        WHERE component_id IN ({ids});
        """
    return execute_db_query(query)


def get_bitbake_vulnerabilities_by_component(id: int):
    """ Возвращает список уязвимостей в компоненте """
    query = f"""
        SELECT *
        FROM bitbake_vulnerabilities
        WHERE component_id = '{id}';
        """
    return execute_db_query(query)


def get_bitbake_vulnerabilities_count_in_component(component_id):
    """ Возвращает список уязвимостей в компоненте """
    query = f"""
        SELECT COUNT(*) FROM bitbake_vulnerabilities
        WHERE component_id = '{component_id}';
        """
    count = execute_db_query(query)[0]['COUNT(*)']
    return count


def add_bitbake_vulnerabilities(data_list: list):
    """в data_list ожидаемся список значений в формате [[component_id, cve, status, summary, cvss_v2, cvss_v3, severity, vector, more_information], [] ]"""
    query = f"""
            INSERT INTO bitbake_vulnerabilities ('component_id', 'cve', 'status', 'summary', 'cvss_v2', 'cvss_v3', 'severity', 'vector', 'more_information') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
    return execute_db_query(query, data_list)
