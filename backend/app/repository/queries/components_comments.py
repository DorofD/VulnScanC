from app.repository.queries.base_query import execute_db_query


def add_comment(user_id, component_id, datetime, comment):
    query = f"""
            INSERT INTO components_comments ('user_id', 'component_id', 'datetime', 'comment') VALUES  ('{user_id}', '{component_id}', '{datetime}', '{comment}');
            """
    return execute_db_query(query)


def get_comments_for_component(component_id):
    query = f"""
            SELECT cc.*, u.login AS user_name
            FROM components_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.component_id = '{component_id}'
            """
    return execute_db_query(query)


def delete_comment(id):
    query = f"""
            DELETE FROM components_comments
            WHERE id = {id};
            """
    return execute_db_query(query)
