from app.repository.queries.base_query import execute_db_query


def add_license(component_id, key, name, spdx_id, url):
    query = f"""
            INSERT INTO licenses ('component_id', 'key', 'name', 'spdx_id', 'url') VALUES ('{component_id}', '{key}', '{name}', '{spdx_id}', '{url}');
            """
    return execute_db_query(query)


def get_component_licenses(component_id):
    query = f"""
            SELECT * FROM licenses
            WHERE component_id = '{component_id}'
            """
    return execute_db_query(query)


def delete_license(id):
    query = f"""
            DELETE FROM licenses 
            WHERE id = {id};
            """
    execute_db_query(query)
