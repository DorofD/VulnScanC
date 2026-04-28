from app.pg_repository.queries.base_query import execute_query

class DBBitbakeComponentsComments():
    def __init__(self):
        pass

    def add_bitbake_component_comment(self, user_id: int, component_id: int, datetime_str: str, comment: str):
        query = """
            INSERT INTO bitbake_components_comments (user_id, component_id, datetime, comment)
            VALUES (%s, %s, %s, %s)
        """
        return execute_query(query, params=(user_id, component_id, datetime_str, comment))

    def get_bitbake_comments_for_component(self, component_id: int):
        query = """
            SELECT cc.*, u.login AS user_name
            FROM bitbake_components_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.component_id = %s
        """
        return execute_query(query, params=(component_id,), fetch="all")

    def delete_bitbake_component_comment(self, comment_id: int):
        query = "DELETE FROM bitbake_components_comments WHERE id = %s"
        return execute_query(query, params=(comment_id,))
