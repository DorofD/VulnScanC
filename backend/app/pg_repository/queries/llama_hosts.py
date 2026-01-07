from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBLlamaHosts:
    def __init__(self):
        pass

    def get_hosts(self):
        query = "SELECT * FROM llama_hosts"
        return execute_query(query, fetch="all")

    def add_host(self, api_url: str, model_type: str, name: str = "",  description: str = ""):
        # чтобы метод реально “что-то возвращал”, добавляем RETURNING
        query = """
            INSERT INTO llama_hosts (name, api_url, model_type, description)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        """
        params = (name, api_url, model_type, description)
        return execute_query(query, params=params, fetch="one")

    def update_host_field(self, id: int, field: str, value: str):
        query = sql.SQL("""
            UPDATE llama_hosts
            SET {field} = %s
            WHERE id = %s
            RETURNING *
        """).format(field=sql.Identifier(field))

        params = (value, id)
        return execute_query(query, params=params, fetch="one")

    def delete_host(self, id: int):
        # чтобы понимать, что удалилось (или что не найдено), вернём удалённую строку
        query = "DELETE FROM llama_hosts WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
