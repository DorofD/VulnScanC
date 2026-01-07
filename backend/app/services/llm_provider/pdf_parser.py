import re
import json
import pdfplumber
import tiktoken


def chunk_text_by_tokens(text: str, max_tokens: int = 300, overlap_tokens: int = 30,
                         encoding_name: str = "cl100k_base"):
    enc = tiktoken.get_encoding(encoding_name)

    # Грубое разбиение на смысловые куски: абзацы/блоки
    parts = [p.strip() for p in re.split(r"\ns*\n+", text) if p.strip()]

    chunks = []
    cur = []
    cur_tokens = 0

    def tok_len(s: str) -> int:
        return len(enc.encode(s))

    for part in parts:
        part_tokens = tok_len(part)

        # Если один абзац сам больше лимита — режем его по токенам в лоб
        if part_tokens > max_tokens:
            # сначала "закрываем" текущий чанк
            if cur:
                chunks.append("\n\n".join(cur))
                cur, cur_tokens = [], 0

            ids = enc.encode(part)
            step = max_tokens
            for i in range(0, len(ids), step):
                piece = enc.decode(ids[i:i + step])
                chunks.append(piece)
            continue

        # Если абзац не помещается — закрываем текущий чанк и начинаем новый
        if cur_tokens + part_tokens > max_tokens and cur:
            chunks.append("\n\n".join(cur))

            # overlap: берем хвост предыдущего чанка в новый (по токенам)
            if overlap_tokens > 0:
                prev_ids = enc.encode(chunks[-1])
                tail = enc.decode(prev_ids[-overlap_tokens:])
                cur = [tail, part]
                cur_tokens = tok_len(tail) + part_tokens
            else:
                cur = [part]
                cur_tokens = part_tokens
        else:
            cur.append(part)
            cur_tokens += part_tokens

    if cur:
        chunks.append("\n\n".join(cur))

    return chunks


# --- извлечение текста из PDF + чанкинг ---
path_pdf = "data/gost56939-2024.pdf"

pages_text = []
with pdfplumber.open(path_pdf) as pdf:
    for page in pdf.pages:
        # if page.page_number == 6:
        #     break
        t = page.extract_text() or ""
        pages_text.append(t)

full_text = "\n\n".join(pages_text)

chunks = chunk_text_by_tokens(full_text, max_tokens=300, overlap_tokens=30)

print("chunks:", len(chunks))
print("first chunk:\n", chunks[0])
# for i in range(len(chunks)):
#     print("Номер чанка:", i)
#     print(chunks[i])

result_data = []
for i in range(len(chunks)):
    # print(chunks[i])
    result_data.append(
        {
            "chunk_number": i,
            "source_document_name": "ГОСТ Р 56939-2024 РБПО",
            "raw_text": chunks[i]
        }
    )

with open('data/output.json', 'w', encoding='utf-8') as f:
    json.dump(result_data, f, ensure_ascii=False, indent=4)
