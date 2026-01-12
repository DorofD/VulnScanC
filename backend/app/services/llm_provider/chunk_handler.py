from app.pg_repository.queries.rag_chunks import DBRagChunks
from app.services.llm_provider.llama_api import Llama
from app.pg_repository.queries.llama_nodes import DBLlamaEmbeddingNodes
import json
from typing import List, Dict, Any, Optional
import re
import pdfplumber
import tiktoken
from typing import List, Iterable


class ChunkHandler:
    def __init__(self):
        self.llama = Llama()
        self.sent_split = re.compile(r"(?<=[.!?…])s+(?=[A-ZА-ЯЁ0-9])")

    def extract_text_from_pdf(self, pdf_file_path):
        # --- извлечение текста из PDF + чанкинг ---
        pdf_file_path = "data/rag_docs/gost_56939_2024.pdf"

        pages_text = []
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                # if page.page_number == 6:
                #     break
                t = page.extract_text() or ""
                pages_text.append(t)

        full_text = "\n\n".join(pages_text)
        return full_text

    def _get_embedding_base_api_url(self) -> str:
        """Return base_api_url from any embedding node (first available).

        Raises RuntimeError if no embedding nodes are configured.
        """
        nodes = DBLlamaEmbeddingNodes().get_nodes() or []
        if not nodes:
            raise RuntimeError(
                "No embedding nodes configured in llama_embedding_nodes")
        # pick the first configured embedding node
        node = nodes[0]
        return node.get('base_api_url')

    def get_embedding_dimension(self):
        """Получить размерность эмбеддинга"""
        base = self._get_embedding_base_api_url()
        dim = len(self.llama.get_embedding(
            "dimension check", base_api_url=base))
        print("Embedding dim =", dim, )
        return dim

    def process_chunks(self, json_path: str, meta_keys: Optional[List[str]] = None) -> None:
        """
        Читает чанки из json, запрашивает embeddings и записывает результат в БД
        meta_keys: какие поля (кроме document_id/raw_text) складывать в meta.
        """
        meta_keys = meta_keys or []

        with open(json_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        print(len(chunks))
        pg_rag = DBRagChunks()
        count = 0
        for ch in chunks:
            count += 1
            raw_text = ch["raw_text"]
            base = self._get_embedding_base_api_url()
            emb = self.llama.get_embedding(raw_text, base_api_url=base)

            meta = {k: ch[k] for k in meta_keys if k in ch}
            print('NUMBER', count)
            pg_rag.upsert_chunk(
                document_id=str(ch["document_id"]),
                raw_text=raw_text,
                embedding=emb,
                meta=meta
            )
            print(f'chunk count done:', count)

    def search_topk(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """
        Возвращает top-k чанков по cosine distance.
        В pgvector оператор:
        embedding <=> query_vector  -- cosine distance (меньше = ближе)
        """
        base = self._get_embedding_base_api_url()
        q_emb = self.llama.get_embedding(query, base_api_url=base)
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

    def build_context_content(self, chunks: list[dict], *, sort_by_id: bool = False) -> str:
        if sort_by_id:
            chunks = sorted(chunks, key=lambda c: c.get("id", 0))

        lines = []
        for c in chunks:
            id = c.get("id", "?")
            source = c.get("document_id", "unknown")
            raw_text = (c.get("raw_text") or "").strip()

            # при желании можно чистить переводы строк внутри чанка:
            raw_text = " ".join(raw_text.split())

            lines.append(
                f"[id: {id} | document_id: {source}] {raw_text}")

        return "CONTEXT:\n" + "\n".join(lines)

    def _split_by_regex(self, text: str, pattern: re.Pattern) -> List[str]:
        parts = pattern.split(text)
        return [p.strip() for p in parts if p and p.strip()]

    def _token_len(self, enc, s: str) -> int:
        return len(enc.encode(s))

    def _slice_by_tokens(self, enc, text: str, max_tokens: int, overlap_tokens: int = 0) -> List[str]:
        ids = enc.encode(text)
        if len(ids) <= max_tokens:
            return [text]

        chunks = []
        step = max_tokens - overlap_tokens if max_tokens > overlap_tokens else max_tokens
        for i in range(0, len(ids), step):
            piece_ids = ids[i:i + max_tokens]
            if not piece_ids:
                break
            chunks.append(enc.decode(piece_ids).strip())
        return [c for c in chunks if c]

    def chunk_text(
        self,
        text: str,
        target_tokens: int = 300,     # желаемый размер
        max_tokens: int = 380,        # жесткий потолок
        min_tokens: int = 120,        # чтобы не плодить мусор
        overlap_tokens: int = 40,
        encoding_name: str = "cl100k_base",
    ) -> List[str]:

        enc = tiktoken.get_encoding(encoding_name)
        enc = tiktoken.get_encoding("cl100k_base")
        text = text.strip()
        if not text:
            return []

        # 1) Крупное разбиение: заголовки (Markdown/похожие) + пустые строки.
        #    Заголовки сохраняем как часть блока (чтобы в чанк попадал контекст).
        #    Простой вариант: сначала режем по двойным переводам строки.
        blocks = [b.strip() for b in re.split(r"\ns*\n+", text) if b.strip()]

        # 2) Если блок слишком большой — дробим на предложения, если всё ещё большой — по токенам.
        atoms: List[str] = []
        for b in blocks:
            if self._token_len(enc, b) <= max_tokens:
                atoms.append(b)
                continue

            # пробуем по предложениям
            sents = self._split_by_regex(b, self.sent_split)
            if len(sents) <= 1:
                # не получилось/это таблица/код — режем по токенам
                atoms.extend(self._slice_by_tokens(
                    enc, b, max_tokens=max_tokens, overlap_tokens=overlap_tokens))
                continue

            # предложения тоже могут быть длинными (редко, но бывает) — подстрахуемся
            for s in sents:
                if self._token_len(enc, s) <= max_tokens:
                    atoms.append(s)
                else:
                    atoms.extend(self._slice_by_tokens(
                        enc, s, max_tokens=max_tokens, overlap_tokens=overlap_tokens))

        # 3) Упаковка атомов в чанки: стараемся попасть в target_tokens,
        #    не превышая max_tokens и не оставляя слишком маленьких хвостов.
        chunks: List[str] = []
        cur_parts: List[str] = []
        cur_tok = 0

        def flush():
            nonlocal cur_parts, cur_tok
            if cur_parts:
                chunks.append("\n\n".join(cur_parts).strip())
                cur_parts, cur_tok = [], 0

        for a in atoms:
            a_tok = self._token_len(enc, a)
            # если текущий пуст — просто добавим
            if not cur_parts:
                cur_parts = [a]
                cur_tok = a_tok
                continue

            # проверяем, поместится ли (учитываем, что добавим еще "\n\n")
            sep_tok = self._token_len(enc, "\n\n")
            projected = cur_tok + sep_tok + a_tok

            if projected <= max_tokens:
                cur_parts.append(a)
                cur_tok = projected
                continue

            # текущий чанк закрываем
            flush()

            # overlap: добавим хвост предыдущего чанка, но только если он осмысленный по размеру
            if overlap_tokens > 0 and chunks:
                prev = chunks[-1]
                prev_ids = enc.encode(prev)
                tail_ids = prev_ids[-overlap_tokens:]
                tail = enc.decode(tail_ids).strip()
                # если хвост слишком короткий — не добавляем, чтобы не плодить мусор
                if self._token_len(enc, tail) >= min_tokens // 2:
                    cur_parts = [tail, a]
                    cur_tok = self._token_len(enc, tail) + sep_tok + a_tok
                else:
                    cur_parts = [a]
                    cur_tok = a_tok
            else:
                cur_parts = [a]
                cur_tok = a_tok

            # если одиночный атом уже > max_tokens (теоретически), добьём токен-слайсингом
            if cur_tok > max_tokens:
                flush()

        flush()

        # 4) Пост-обработка: мерджим слишком маленькие чанки с соседними (если можно)
        merged: List[str] = []
        for c in chunks:
            c_tok = self._token_len(enc, c)
            if merged and c_tok < min_tokens:
                candidate = merged[-1] + "\n\n" + c
                if self._token_len(enc, candidate) <= max_tokens:
                    merged[-1] = candidate
                    continue
            merged.append(c)

        return merged

    def extract_and_chunk(self, pdf_file_path):
        extracted_text = self.extract_text_from_pdf(pdf_file_path)
        chunks = self.chunk_text(extracted_text, target_tokens=350,
                                 max_tokens=430, min_tokens=170, overlap_tokens=60)

        result_data = []
        for i in range(len(chunks)):
            # print(chunks[i])
            result_data.append(
                {
                    "document_id": 1,
                    "raw_text": chunks[i]
                }
            )
        with open(f"data/rag_docs/{pdf_file_path}.json", 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
        return result_data

# print(ChunkHandler().get_embedding_dimension())
# Посчитать эмбеддинги для чанков и сохранить результат
# ChunkHandler().process_chunks('data/rag_docs/output3.json', meta_keys=[])

# Найти топ близких к запросу чанков
# top_chunks = search_topk(
#     "Запрооооос", k=5)
# for i in top_chunks:
#     print(i['id'], i['cosine_similarity'])
