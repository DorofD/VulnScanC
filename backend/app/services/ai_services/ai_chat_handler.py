from app.pg_repository.queries.rag_chunks import DBRagChunks
from app.pg_repository.queries.llama_nodes import DBLlamaEmbeddingNodes, DBLlamaChatNodes
from app.adapters.llama_api import LlamaEmbeddingApiAdapter, LlamaChatApiAdapter
from typing import List, Dict, Any, Optional

from typing import List


class AiChatHandler:
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

    def send_messages(self, messages, use_rag: bool = False):
        # msg_count = len(messages)
        print('message count:', len(messages))
        # ch = Chunker()
        active_node = DBLlamaChatNodes().get_active_node()
        if not active_node:
            return {"error": "Not found active llama node", "status": 400}
        user_text = messages[0]['content']
        if use_rag:
            topk_chunks = self.search_topk(user_text, k=5)

            for i in topk_chunks:
                print(i['cosine_similarity'], i['id'])

            system_prompt_str = "Answer strictly based on CONTEXT. If the CONTEXT is incomplete, then write - 'Not enough data in CONTEXT'. Answer in Russian."
            context_str = self.build_context_content(topk_chunks)

            final_messages = [
                {"role": "system", "content": system_prompt_str},
                {"role": "user", "content": context_str},
                {"role": "user", "content": user_text}
            ]
        else:
            system_prompt_str = "Answer briefly and in Russian."
            final_messages = [
                {"role": "system", "content": system_prompt_str},
                {"role": "user", "content": user_text}
            ]
        base_api = active_node['base_api_url']
        response = LlamaChatApiAdapter(base_api).send_message(
            final_messages)
        if response:
            return response
        return False
