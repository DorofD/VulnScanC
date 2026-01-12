from psycopg2 import sql
from app.pg_repository.queries.base_query import execute_query


class DBRagDocuments:
    def __init__(self):
        pass

    def get_document(self, id: int):
        query = "SELECT * FROM rag_documents WHERE id = %s"
        params = (id,)
        return execute_query(query, params=params, fetch="one")

    def get_documents(self):
        query = "SELECT * FROM rag_documents"
        return execute_query(query, fetch="all")

    def add_document(self, name: str, file_path: str):
        query = """
            INSERT INTO rag_documents (name, file_path)
            VALUES (%s, %s)
            RETURNING *
        """
        params = (name, file_path)
        return execute_query(query, params=params, fetch="one")

    def update_document(self, id: int, name: str, file_path: str):
        query = """
            UPDATE rag_documents
            SET name = %s, file_path = %s
            WHERE id = %s
            RETURNING *
        """
        params = (name, file_path, id)
        return execute_query(query, params=params, fetch="one")

    def delete_document(self, id: int):
        query = "DELETE FROM rag_documents WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
