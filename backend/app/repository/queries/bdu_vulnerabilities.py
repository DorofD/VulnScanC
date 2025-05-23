from app.repository.queries.base_query import execute_db_query


def get_bdu_vulnerabilities(component_type):
    """ Возвращает список уязвимостей в компонентах """
    query = f"""
        SELECT *
        FROM bdu_vulnerabilities
        WHERE component_type = '{component_type}';
        """
    return execute_db_query(query)


def get_bdu_vulnerabilities_by_components(id_list: list, component_type: str):
    """ Возвращает список уязвимостей в компонентах """
    ids = ', '.join(map(str, id_list))
    query = f"""
        SELECT *
        FROM bdu_vulnerabilities
        WHERE component_id IN ({ids}) AND component_type = '{component_type}';
        """
    return execute_db_query(query)


def get_bdu_vulnerabilities_by_component(id: int, component_type: str):
    """ Возвращает список уязвимостей в компонентах """
    query = f"""
        SELECT *
        FROM bdu_vulnerabilities
        WHERE component_id = '{id}' AND component_type = '{component_type}';
        """
    return execute_db_query(query)


def get_bdu_vulnerabilities_count():
    """ Возвращает список уязвимостей в компонентах """
    query = f"""
        SELECT COUNT(*) FROM bdu_vulnerabilities
        """
    count = execute_db_query(query)[0]['COUNT(*)']
    return count


def get_bdu_vulnerabilities_count_in_component(component_id: int, component_type: str):
    """ Возвращает список уязвимостей в компоненте """
    query = f"""
        SELECT COUNT(*) FROM bdu_vulnerabilities
        WHERE component_id = '{component_id}' AND component_type = '{component_type}';
        """
    count = execute_db_query(query)[0]['COUNT(*)']
    return count


def add_bdu_vulnerabilities(data_list: list):
    """в data_list ожидаемся список значений в формате [{component_id: .., component_type: .., bdu_id: .., cve_id: .., name: .., description: .., status: .., bdu_severity: .., severity: ..}]"""
    query = f"""
        INSERT INTO bdu_vulnerabilities ('component_id', 'component_type', 'bdu_id', 'cve_id', 'name', 'description', 'status', 'bdu_severity', 'severity') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
    return execute_db_query(query, data_list)
