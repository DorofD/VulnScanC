import json
from pgvector import Vector
from typing import List, Dict, Any, Optional
from app.pg_repository.queries.base_query import execute_query


class DBRagChunks:
    def __init__(self):
        pass

    def upsert_chunk(self,
                     document_id: int,
                     raw_text: str,
                     embedding: List[float],
                     meta: Optional[Dict[str, Any]] = None,
                     ) -> None:

        execute_query(
            """
                INSERT INTO rag_chunks (document_id, raw_text, meta, embedding)
                VALUES (%s, %s, %s, %s)
            """,
            (document_id, raw_text,
             json.dumps(meta), Vector(embedding)), fetch=None
        )

    def search_topk(self, query_embedding, k: int = 5) -> List[Dict[str, Any]]:
        """
        Возвращает top-k чанков по cosine distance.
        В pgvector оператор:
        embedding <=> query_vector  -- cosine distance (меньше = ближе)
        """

        result = execute_query(
            """
                SELECT
                id,
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

    def get_chunks_by_document_id(self, document_id: int) -> List[Dict[str, Any]]:
        """
            Возвращает все чанки с указанным document_id.
            """
        result = execute_query(
            """
            SELECT
            id,
            document_id,
            raw_text,
            meta,
            FROM rag_chunks
            WHERE document_id= % s
            ORDER BY id;
            """,
            (document_id,),
            fetch="all"
        )
        return result
