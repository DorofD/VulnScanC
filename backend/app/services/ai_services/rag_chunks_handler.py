from app.pg_repository.queries.rag_chunks import DBRagChunks
from app.pg_repository.queries.llama_nodes import DBLlamaEmbeddingNodes, DBLlamaChatNodes
from app.adapters.pdf_extract import PDFExtractAdapter
from app.adapters.chunker import Chunker
from app.adapters.llama_api import LlamaEmbeddingApiAdapter, LlamaChatApiAdapter
from typing import List, Dict, Any, Optional

from typing import List


class RagChatHandler:
    def __init__(self):
        self.base_embed_url = self.get_embedding_base_api_url()
        self.embed_adapter = LlamaEmbeddingApiAdapter(self.base_embed_url)

    def get_embedding_base_api_url(self) -> str:
        # For simplicity, we use the first embedding node found.
        pg_embedding = DBLlamaEmbeddingNodes()
        node = pg_embedding.get_nodes()
        if not node:
            raise RuntimeError('No embedding nodes configured')
        base_api_url = node[0]['base_api_url']
        return base_api_url

    def cut_pdf_to_chunks(self, pdf_path, document_id, meta_keys: Optional[List[str]] = None) -> None:
        """
        Читает чанки из json, запрашивает embeddings и записывает результат в БД
        meta_keys: какие поля (кроме document_id/raw_text) складывать в meta.
        """
        meta_keys = meta_keys or []
        pdf_ex = PDFExtractAdapter()
        full_text = pdf_ex.extract_text(pdf_path)
        chunker = Chunker()
        chunks = chunker.chunk_text(full_text)
        print(len(chunks))

        pg_rag = DBRagChunks()
        llama_embed = LlamaEmbeddingApiAdapter(self.base_embed_url)
        count = 0
        for ch in chunks:
            count += 1
            raw_text = ch["raw_text"]
            emb = llama_embed.get_embedding(raw_text)

            meta = {k: ch[k] for k in meta_keys if k in ch}
            print('NUMBER', count)
            pg_rag.upsert_chunk(
                document_id=document_id,
                raw_text=raw_text,
                embedding=emb,
                meta=meta
            )
            print('NUMBER', count, 'DONE')

    def search_topk(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """
        Возвращает top-k чанков по cosine distance.
        В pgvector оператор:
        embedding <=> query_vector  -- cosine distance (меньше = ближе)
        """
        q_emb = self.embed_adapter.get_embedding(query)
        pg_rag = DBRagChunks()

        rows = pg_rag.search_topk(q_emb, k)
        results = []
        for row in rows:
            results.append(
                {
                    "id": row['id'],
                    "raw_text": row['raw_text'],
                    "meta": row['meta'],
                    "cosine_similarity": float(row['cosine_similarity']),
                }
            )
        return results

    def build_context_content(self, chunks: list[dict]) -> str:
        lines = []
        for c in chunks:
            raw_text = (c.get("raw_text") or "").strip()
            raw_text = " ".join(raw_text.split())

            lines.append(
                # f"[id: {id} | document_id: {source}] {raw_text}")
                f"|{raw_text}|")

        return "CONTEXT:\n" + "\n".join(lines)

    def send_messages(self, messages, chat_node_uuid: str = None):
        # msg_count = len(messages)
        print('message count:', len(messages))
        # ch = Chunker()
        if chat_node_uuid:
            host_info = DBLlamaChatNodes().get_node_by_uuid(chat_node_uuid)
            if not host_info:
                return {"error": "model not found", "status": 400}
        user_text = messages[0]['content']
        topk_chunks = self.search_topk(user_text, k=5)

        for i in topk_chunks:
            print(i['cosine_similarity'], i['id'])

        system_prompt_str = "Ты специалист DevSecOps, отвечай строго на основе CONTEXT, если в CONTEXT нет ответа - напиши, что ответ не найден"
        context_str = self.build_context_content(topk_chunks)

        final_messages = [
            {"role": "system", "content": system_prompt_str},
            {"role": "user", "content": context_str},
            {"role": "user", "content": user_text}

        ]
        base_api = host_info['base_api_url']
        response = LlamaChatApiAdapter(base_api).send_message(
            final_messages)
        if response:
            return response
        return False
