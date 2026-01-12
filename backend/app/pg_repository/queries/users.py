from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBUsers:
    def __init__(self):
        pass

    def get_users(self):
        query = "SELECT * FROM users"
        return execute_query(query, fetch="all")

    def get_user(self, login: str):
        query = f"SELECT * FROM users WHERE login = %s"
        params = (login,)
        return execute_query(query, params, fetch="one")

    def add_user(self, login: str, auth_type: str, role: str, password: str = ""):
        query = """
            INSERT INTO users (login, auth_type, role, password)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        """
        params = (login, auth_type, role, password)
        return execute_query(query, params=params, fetch="one")

    def update_user_field(self, id: int, field: str, value: str):
        query = sql.SQL("""
            UPDATE users
            SET {field} = %s
            WHERE id = %s
            RETURNING *
        """).format(field=sql.Identifier(field))

        params = (value, id)
        return execute_query(query, params=params, fetch="one")

    def delete_user(self, id: int):
        # чтобы понимать, что удалилось (или что не найдено), вернём удалённую строку
        query = "DELETE FROM users WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
