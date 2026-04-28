from app.pg_repository.queries.base_query import execute_query

class DBBitbakeVulnerabilities():
    def __init__(self):
        pass

    def get_bitbake_vulnerabilities_ids(self):
        """ Возвращает cve и component_id уязвимостей со статусом Unpatched"""
        query = "SELECT cve, component_id FROM bitbake_vulnerabilities WHERE status = 'Unpatched'"
        return execute_query(query, fetch="all")

    def get_bitbake_vulnerabilities_by_components(self, id_list: list):
        """ Возвращает список уязвимостей в компонентах """
        query = "SELECT * FROM bitbake_vulnerabilities WHERE component_id IN %s"
        params = (tuple(id_list),)
        return execute_query(query, params=params, fetch="all")

    def get_bitbake_vulnerabilities_by_component(self, component_id: int):
        """ Возвращает список уязвимостей в компоненте """
        query = "SELECT * FROM bitbake_vulnerabilities WHERE component_id = %s"
        return execute_query(query, params=(component_id,), fetch="all")

    def get_bitbake_vulnerabilities_count_in_component(self, component_id: int):
        """ Возвращает количество уязвимостей в компоненте """
        query = "SELECT COUNT(*) as count FROM bitbake_vulnerabilities WHERE component_id = %s"
        result = execute_query(query, params=(component_id,), fetch="one")
        return result[0]['count'] if result and result[0] else 0

    def add_bitbake_vulnerabilities(self, data_list: list):
        """в data_list ожидаемся список значений в формате [[component_id, cve, status, summary, cvss_v2, cvss_v3, severity, vector, more_information], [] ]"""
        query = """
            INSERT INTO bitbake_vulnerabilities (component_id, cve, status, summary, cvss_v2, cvss_v3, severity, vector, more_information)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # execute_query handles multiple rows if data_list is a list of tuples/lists
        return execute_query(query, params=data_list)
