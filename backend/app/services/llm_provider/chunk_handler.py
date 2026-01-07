from app.pg_repository.queries.rag import PostgresRAG
from app.services.llm_provider.llama_api import Llama
import json
from typing import List, Dict, Any, Optional


class ChunkHandler:
    def __init__(self):
        self.llama = Llama()

    def get_embedding_dimension(self):
        """Получить размерность эмбеддинга"""
        dim = len(self.llama.get_embedding("dimension check"))
        print("Embedding dim =", dim)
        return dim

    def process_chunks(self, json_path: str, meta_keys: Optional[List[str]] = None) -> None:
        """
        Читает чанки из json, запрашивает embeddings и записывает результат в БД
        meta_keys: какие поля (кроме chunk_number/source_document_name/raw_text) складывать в meta.
        """
        meta_keys = meta_keys or []

        with open(json_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        print(len(chunks))
        pg_rag = PostgresRAG()
        for i, ch in enumerate(chunks, start=1):
            raw_text = ch["raw_text"]
            emb = self.llama.get_embedding(raw_text)

            meta = {k: ch[k] for k in meta_keys if k in ch}
            print('NUMBER', ch["chunk_number"])
            pg_rag.upsert_chunk(
                chunk_number=ch["chunk_number"],
                source_document_name=str(ch["source_document_name"]),
                raw_text=raw_text,
                embedding=emb,
                meta=meta
            )
            print(f'chunk number {ch["chunk_number"]} done')

    def search_topk(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """
        Возвращает top-k чанков по cosine distance.
        В pgvector оператор:
        embedding <=> query_vector  -- cosine distance (меньше = ближе)
        """
        q_emb = self.llama.get_embedding(query)
        pg_rag = PostgresRAG()

        rows = pg_rag.search_topk(q_emb, k)
        results = []
        for row in rows:
            results.append(
                {
                    "chunk_number": row['chunk_number'],
                    "source_document_name": row['source_document_name'],
                    "raw_text": row['raw_text'],
                    "meta": row['meta'],
                    "cosine_similarity": float(row['cosine_similarity']),
                }
            )
        return results

    def build_context_content(self, chunks: list[dict], *, sort_by_chunk_number: bool = False) -> str:
        if sort_by_chunk_number:
            chunks = sorted(chunks, key=lambda c: c.get("chunk_number", 0))

        lines = []
        for c in chunks:
            chunk_number = c.get("chunk_number", "?")
            source = c.get("source_document_name", "unknown")
            raw_text = (c.get("raw_text") or "").strip()

            # при желании можно чистить переводы строк внутри чанка:
            raw_text = " ".join(raw_text.split())

            lines.append(
                f"[chunk_number: {chunk_number} | source_document_name: {source}] {raw_text}")

        return "CONTEXT:\n" + "\n".join(lines)


# print(ChunkHandler().get_embedding_dimension())
# Посчитать эмбеддинги для чанков и сохранить результат
# ChunkHandler().process_chunks('data/output2.json', meta_keys=[])

# Найти топ близких к запросу чанков
# top_chunks = search_topk(
#     "Запрооооос", k=5)
# for i in top_chunks:
#     print(i['chunk_number'], i['cosine_similarity'])

#     # 4) Поиск
#     res = search_topk(
#         conn, "Какие процедуры информирования пользователей описаны?", k=4)
#     for r in res:
#         print(r["cosine_similarity"],
#               r["source_document_name"], r["chunk_number"])
#         print(r["raw_text"][:300])
#         print("---")
