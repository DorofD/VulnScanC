from app.pg_repository.queries.base_query import execute_query


class DBComponentsComments:
    @staticmethod
    def add_comment(user_id, component_id, datetime, comment):
        query = """
            INSERT INTO components_comments (user_id, component_id, datetime, comment)
            VALUES (%s, %s, %s, %s);
        """
        return execute_query(query, (user_id, component_id, datetime, comment))

    @staticmethod
    def get_comments_for_component(component_id):
        query = """
            SELECT cc.*, u.login AS user_name
            FROM components_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.component_id = %s;
        """
        return execute_query(query, (component_id,))

    @staticmethod
    def delete_comment(id):
        query = """
            DELETE FROM components_comments
            WHERE id = %s;
        """
        return execute_query(query, (id,))
