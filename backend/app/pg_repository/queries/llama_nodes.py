from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBLlamaChatNodes:
    def __init__(self):
        pass

    def get_nodes(self):
        query = "SELECT * FROM llama_chat_nodes ORDER BY is_active DESC, uuid;"
        return execute_query(query, fetch="all")

    def get_node_by_uuid(self, uuid: str):
        query = "SELECT * FROM llama_chat_nodes WHERE uuid = %s"
        params = (uuid,)
        return execute_query(query, params=params, fetch="one")

    def get_node_by_id(self, id: int):
        query = "SELECT * FROM llama_chat_nodes WHERE id = %s"
        params = (id,)
        return execute_query(query, params=params, fetch="one")

    def add_node(self, base_api_url: str, name: str = "", description: str = ""):
        query = """
            INSERT INTO llama_chat_nodes (name, base_api_url, description)
            VALUES (%s, %s, %s)
            RETURNING *
        """
        params = (name, base_api_url, description)
        return execute_query(query, params=params, fetch="one")

    def update_node_field(self, id: int, field: str, value: str):
        query = sql.SQL("""
            UPDATE llama_chat_nodes
            SET {field} = %s
            WHERE id = %s
            RETURNING *
        """).format(field=sql.Identifier(field))

        params = (value, id)
        return execute_query(query, params=params, fetch="one")

    def delete_node(self, id: int):
        query = "DELETE FROM llama_chat_nodes WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")

    def set_active_by_uuid(self, node_uuid: str):
        query = """
        WITH
        deactivated AS (
            UPDATE llama_chat_nodes
            SET is_active = false
            WHERE is_active = true
              AND uuid <> %s
            RETURNING 1
        ),
        activated AS (
            UPDATE llama_chat_nodes n
            SET is_active = true
            FROM (SELECT 1) s
            LEFT JOIN deactivated d ON true 
            WHERE n.uuid = %s
            RETURNING n.*
        )
        SELECT * FROM activated;
        """
        params = (node_uuid, node_uuid)
        return execute_query(query, params=params, fetch="one")

    def get_active_node(self):
        """
        Возвращает единственную активную запись
        """
        query = "SELECT * FROM llama_chat_nodes WHERE is_active = true"
        return execute_query(query, fetch="one")


class DBLlamaEmbeddingNodes:
    def __init__(self):
        pass

    def get_nodes(self):
        query = "SELECT * FROM llama_embedding_nodes"
        return execute_query(query, fetch="all")

    def get_node_by_uuid(self, uuid: str):
        query = "SELECT * FROM llama_embedding_nodes WHERE uuid = %s"
        params = (uuid,)
        return execute_query(query, params=params, fetch="one")

    def get_node_by_id(self, id: int):
        query = "SELECT * FROM llama_embedding_nodes WHERE id = %s"
        params = (id,)
        return execute_query(query, params=params, fetch="one")

    def add_node(self, base_api_url: str, name: str = "", description: str = ""):
        query = """
            INSERT INTO llama_embedding_nodes (name, base_api_url, description)
            VALUES (%s, %s, %s)
            RETURNING *
        """
        params = (name, base_api_url, description)
        return execute_query(query, params=params, fetch="one")

    def update_node_field(self, id: int, field: str, value: str):
        query = sql.SQL("""
            UPDATE llama_embedding_nodes
            SET {field} = %s
            WHERE id = %s
            RETURNING *
        """).format(field=sql.Identifier(field))

        params = (value, id)
        return execute_query(query, params=params, fetch="one")

    def delete_node(self, id: int):
        query = "DELETE FROM llama_embedding_nodes WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
