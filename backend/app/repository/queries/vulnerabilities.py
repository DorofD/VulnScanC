from app.repository.queries.base_query import execute_db_query


def get_vulnerabilities_ids():
    """ Возвращает osv_id и component_id уязвимостей """
    query = f"""
        SELECT osv_id, component_id
        FROM vulnerabilities;
        """
    return execute_db_query(query)


def get_vulnerabilities_by_components(id_list: list):
    """ Возвращает список уязвимостей в компонентах """
    ids = ', '.join(map(str, id_list))
    query = f"""
        SELECT *
        FROM vulnerabilities
        WHERE component_id IN ({ids});
        """
    return execute_db_query(query)


def get_vulnerabilities_by_component(id: int):
    """ Возвращает список уязвимостей в компонентах """
    query = f"""
        SELECT *
        FROM vulnerabilities
        WHERE component_id = '{id}';
        """
    return execute_db_query(query)


def add_vulnerabilities(data_list: list):
    """в data_list ожидаемся список значений в формате [{component_id: ..., osv_id: ..., full_data: ...}]"""
    query = f"""
            INSERT INTO vulnerabilities ('component_id', 'osv_id', 'full_data') VALUES (?, ?, ?);
            """
    return execute_db_query(query, data_list)
