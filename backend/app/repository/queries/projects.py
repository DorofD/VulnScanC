from app.repository.queries.base_query import execute_db_query


def add_project(name):
    query = f"""
            INSERT INTO projects ('name') VALUES('{name}');
            """
    return execute_db_query(query)


def get_projects():
    query = f"""
            SELECT * FROM projects
            """
    return execute_db_query(query)


def get_project(name):
    """ Возвращает проект по имени """
    query = f"""
            SELECT * FROM projects
            WHERE name = '{name}'
            """
    return execute_db_query(query)


def change_project(id, name):
    query = f"""
            UPDATE projects
            SET name = '{name}'
            WHERE id = {id};
            """
    return execute_db_query(query)


def delete_project(id):
    query = f"""
            DELETE FROM vulnerabilities 
            WHERE component_id IN (
                SELECT id FROM components WHERE project_id = {id}
            );
            """
    execute_db_query(query)

    query = f"""
            DELETE FROM components WHERE project_id = {id};
            """
    execute_db_query(query)

    query = f"""
            DELETE FROM snapshots WHERE project_id = {id};
            """
    execute_db_query(query)

    query = f"""
            DELETE FROM projects WHERE id = {id};
            """
    execute_db_query(query)


# delete_project(1)
