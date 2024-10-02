from app.repository.queries.base_query import execute_db_query


def get_component(id):
    query = f"""
                SELECT * FROM components WHERE id = '{id}'; 
            """
    return execute_db_query(query)


def get_project_components(project_id: int):
    """ Возвращает список компонентов по id проекта """
    query = f"""
            SELECT components.*
            FROM components
            JOIN projects ON components.project_id = projects.id
            WHERE projects.id = '{project_id}';
            """
    return execute_db_query(query)


def add_component(project_id: int, path: str, type: str = None, address: str = None, tag: str = None, version: str = None, score: float = None):
    query = f"""
            INSERT INTO components ('project_id', 'path', 'type', 'address', 'tag', 'version', 'score', 'status')
            VALUES ('{project_id}', '{path}', '{type}', '{address}', '{tag}', '{version}', '{score}', 'none');
            """
    return execute_db_query(query)


def change_component_status(id, new_status):
    """ Возможные статусы: none, confirmed, denied"""
    query = f"""
            UPDATE components
            SET status = '{new_status}'
            WHERE id = {id};
            """
    return execute_db_query(query)
