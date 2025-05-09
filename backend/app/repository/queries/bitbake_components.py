from app.repository.queries.base_query import execute_db_query


def get_bitbake_component(id):
    query = f"""
                SELECT * FROM bitbake_components WHERE id = '{id}'; 
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


# def add_bitbake_component(project_id: int, name: str, version: str = None, layer: str = None):
#     query = f"""
#             INSERT INTO bitbake_components ('project_id', 'name', 'version', 'layer')
#             VALUES ('{project_id}', '{name}', '{version}', '{layer}');
#             """
#     return execute_db_query(query)


def add_bitbake_components(data_list: list):
    """в data_list ожидаемся список значений в формате [[project_id, name, version, layer], ...]"""
    query = f"""
            INSERT INTO bitbake_components ('project_id', 'name', 'version', 'layer') VALUES (?, ?, ?, ?);
            """
    return execute_db_query(query, data_list)
