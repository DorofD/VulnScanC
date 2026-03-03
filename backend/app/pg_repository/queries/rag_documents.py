from app.pg_repository.queries.base_query import execute_query
import uuid


class DBRagDocuments:
    def __init__(self):
        pass

    def get_document(self, id: int):
        query = """
            SELECT d.id, d.uuid, d.name, d.file_path, d.description,
                COUNT(c.id) AS chunks_num
            FROM rag_documents d
            LEFT JOIN rag_chunks c ON c.document_id = d.id
            WHERE d.id = %s
            GROUP BY d.id, d.uuid, d.name, d.file_path, d.description
        """
        return execute_query(query, params=(id,), fetch="one")

    def get_documents(self):
        query = """
            SELECT d.id, d.uuid, d.name, d.file_path, d.description,
                (SELECT COUNT(*) FROM rag_chunks c WHERE c.document_id = d.id) AS chunks_num
            FROM rag_documents d
        """
        return execute_query(query, fetch="all")

    def add_document(self, name: str, description: str = None):
        print(description)
        query = """
            INSERT INTO rag_documents (name, description)
            VALUES (%s, %s)
            RETURNING *
            """
        params = (name, description)
        return execute_query(query, params=params, fetch="one")

    def update_document(self, id: int, name: str, file_path: str, description: str = None):
        query = """
            UPDATE rag_documents
            SET name = %s,
                file_path = %s,
                description = %s
            WHERE id = %s
            RETURNING id, uuid, name, file_path, description
        """
        return execute_query(query, params=(name, file_path, description, id), fetch="one")

    def delete_document(self, id: int):
        query = "DELETE FROM rag_documents WHERE id = %s RETURNING *"
        params = (id,)
        return execute_query(query, params=params, fetch="one")
