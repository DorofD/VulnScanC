from app.repository.queries.base_query import execute_db_query


def get_users_db():
    query = f"""
            SELECT * FROM users
            """
    return execute_db_query(query)


def get_user_db(login: str):
    query = f"""
            SELECT * FROM users
            WHERE login = '{login}'
            """
    return execute_db_query(query)


def add_user_db(login: str, auth_type: str, role: str,  password: str = ''):

    query = f"""
            INSERT INTO users ('login', 'auth_type', 'role', 'password') VALUES('{login}', '{auth_type}', '{role}', '{password}');
            """
    return execute_db_query(query)


def change_user_db(id: int, changes: dict):

    query = "UPDATE users SET "
    updates = []
    for column, value in changes.items():
        updates.append(f"{column} = '{value}'")
    query += ", ".join(updates)
    query += f" WHERE id = '{id}';"

    return execute_db_query(query)


def delete_user_db(id: int):
    query = f"""
            DELETE FROM users
            WHERE id = '{id}'
            """
    return execute_db_query(query)
