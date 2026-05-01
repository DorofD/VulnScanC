from app.pg_repository.queries.base_query import execute_query


class DBVulnerabilities():
    def __init__(self):
        pass

    def get_vulnerabilities_ids(self):
        """ Возвращает osv_id и component_id уязвимостей """
        query = "SELECT osv_id, component_id FROM vulnerabilities"
        return execute_query(query, fetch="all")

    def get_vulnerabilities_by_components(self, id_list: list):
        """ Возвращает список уязвимостей в компонентах """
        query = "SELECT * FROM vulnerabilities WHERE component_id IN %s"
        params = (tuple(id_list),)
        return execute_query(query, params=params, fetch="all")

    def get_vulnerabilities_by_component(self, component_id: int):
        """ Возвращает список уязвимостей в компонентах """
        query = "SELECT * FROM vulnerabilities WHERE component_id = %s"
        return execute_query(query, params=(component_id,), fetch="all")

    def get_vulnerabilities_count_in_component(self, component_id: int):
        """ Возвращает количество уязвимостей в компоненте """
        query = "SELECT COUNT(*) as count FROM vulnerabilities WHERE component_id = %s"
        result = execute_query(query, params=(component_id,), fetch="one")
        return result['count']

    def add_vulnerabilities(self, data_list: list):
        """
        data_list: list of dicts [{'component_id': ..., 'osv_id': ..., 'full_data': ...}]
        """
        query = "INSERT INTO vulnerabilities (component_id, osv_id, full_data) VALUES (%s, %s, %s)"
        for item in data_list:
            execute_query(query, params=(
                item['component_id'], item['osv_id'], item['full_data']))
