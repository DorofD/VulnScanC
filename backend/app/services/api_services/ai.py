from app.services.llm_provider.llama_api import Llama
from app.services.llm_provider.chunk_handler import ChunkHandler


def send_messages(messages):
    msg_count = len(messages)
    # print(messages)

    llama = Llama()
    ch = ChunkHandler()
    if msg_count == 1:
        user_text = messages[0]['content']
        topk_chunks = ch.search_topk(user_text, k=5)

        for i in topk_chunks:
            print(i['chunk_number'], i['cosine_similarity'])

        system_prompt_str = "Ты специалист по ИБ, отвечай строго на основе CONTEXT, если в CONTEXT нет ответа - так и скажи"
        context_str = build_context_content(topk_chunks)
        # print(context_str)

        final_messages = [
            {"role": "system", "content": system_prompt_str},
            {"role": "user", "content": context_str},
            {"role": "user", "content": user_text}

        ]
        response = llama.send_message(final_messages)
        if response:
            return response
        return False
    return False


def build_context_content(chunks: list[dict], *, sort_by_chunk_number: bool = False) -> str:
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
