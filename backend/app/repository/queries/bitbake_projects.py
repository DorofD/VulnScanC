from app.repository.queries.base_query import execute_db_query


def add_bitbake_project(name):
    query = f"""
            INSERT INTO bitbake_projects ('name') VALUES('{name}');
            """
    return execute_db_query(query)


def get_bitbake_projects():
    query = f"""
            SELECT * FROM bitbake_projects
            """
    return execute_db_query(query)


def get_bitbake_project(name):
    """ Возвращает проект по имени """
    query = f"""
            SELECT * FROM bitbake_projects
            WHERE name = '{name}'
            """
    return execute_db_query(query)


def change_bitbake_project(id, name):
    query = f"""
            UPDATE bitbake_projects
            SET name = '{name}'
            WHERE id = {id};
            """
    return execute_db_query(query)


def delete_bitbake_project(id):
    query = f"""
            DELETE FROM bitbake_vulnerabilities 
            WHERE component_id IN (
                SELECT id FROM bitbake_components WHERE project_id = {id}
            );
            """
    execute_db_query(query)

    query = f"""
            DELETE FROM bitbake_components WHERE project_id = {id};
            """
    execute_db_query(query)

    query = f"""
            DELETE FROM bitbake_snapshots WHERE project_id = {id};
            """
    execute_db_query(query)

    query = f"""
            DELETE FROM bitbake_projects WHERE id = {id};
            """
    execute_db_query(query)
