from app.repository.queries.base_query import execute_db_query


def get_bdu_vulnerabilities():
    """ Возвращает список уязвимостей в компонентах """
    query = f"""
        SELECT *
        FROM bdu_vulnerabilities;
        """
    return execute_db_query(query)


def get_bdu_vulnerabilities_by_components(id_list: list):
    """ Возвращает список уязвимостей в компонентах """
    ids = ', '.join(map(str, id_list))
    query = f"""
        SELECT *
        FROM bdu_vulnerabilities
        WHERE component_id IN ({ids});
        """
    return execute_db_query(query)


def get_bdu_vulnerabilities_by_component(id: int):
    """ Возвращает список уязвимостей в компонентах """
    query = f"""
        SELECT *
        FROM bdu_vulnerabilities
        WHERE component_id = '{id}';
        """
    return execute_db_query(query)


def get_bdu_vulnerabilities_count():
    """ Возвращает список уязвимостей в компонентах """
    query = f"""
        SELECT COUNT(*) FROM bdu_vulnerabilities
        """
    count = execute_db_query(query)[0]['COUNT(*)']
    return count


def add_bdu_vulnerabilities(data_list: list):
    """в data_list ожидаемся список значений в формате [{component_id: .., bdu_id: .., cve_id: .., name: .., description: .., status: .., bdu_severity: .., severity: ..}]"""
    query = f"""
        INSERT INTO bdu_vulnerabilities ('component_id', 'bdu_id', 'cve_id', 'name', 'description', 'status', 'bdu_severity', 'severity') VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
    return execute_db_query(query, data_list)
