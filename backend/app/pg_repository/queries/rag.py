import json
from psycopg2 import sql
from pgvector.psycopg2 import register_vector
from pgvector import Vector
from typing import List, Dict, Any, Optional
from app.pg_repository.queries.base_query import execute_query


class PostgresRAG:
    def __init__(self):
        pass

    def upsert_chunk(self,
                     chunk_number: int,
                     source_document_name: str,
                     raw_text: str,
                     embedding: List[float],
                     meta: Optional[Dict[str, Any]] = None,
                     ) -> None:

        execute_query(
            """
                INSERT INTO rag_chunks (chunk_number, source_document_name, raw_text, meta, embedding)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (source_document_name, chunk_number)
                DO UPDATE SET
                raw_text = EXCLUDED.raw_text,
                meta = EXCLUDED.meta,
                embedding = EXCLUDED.embedding
            """,
            (chunk_number, source_document_name, raw_text,
             json.dumps(meta), Vector(embedding)), fetch=None
        )

    def search_topk(self, query_embedding, k: int = 4) -> List[Dict[str, Any]]:
        """
        Возвращает top-k чанков по cosine distance.
        В pgvector оператор:
        embedding <=> query_vector  -- cosine distance (меньше = ближе)
        """

        result = execute_query(
            """
                SELECT
                chunk_number,
                source_document_name,
                raw_text,
                meta,
                (1 - (embedding <=> %s)) AS cosine_similarity
                FROM rag_chunks
                ORDER BY embedding <=> %s
                LIMIT %s;
                """,
            (Vector(query_embedding), Vector(query_embedding), k),
            fetch="all"
        )
        return result
