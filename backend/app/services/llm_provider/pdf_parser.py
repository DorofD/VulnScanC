import re
import json
import pdfplumber
import tiktoken
from typing import List, Iterable

_SENT_SPLIT = re.compile(r"(?<=[.!?…])s+(?=[A-ZА-ЯЁ0-9])")


def _split_by_regex(text: str, pattern: re.Pattern) -> List[str]:
    parts = pattern.split(text)
    return [p.strip() for p in parts if p and p.strip()]


def _token_len(enc, s: str) -> int:
    return len(enc.encode(s))


def _slice_by_tokens(enc, text: str, max_tokens: int, overlap_tokens: int = 0) -> List[str]:
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
        if _token_len(enc, b) <= max_tokens:
            atoms.append(b)
            continue

        # пробуем по предложениям
        sents = _split_by_regex(b, _SENT_SPLIT)
        if len(sents) <= 1:
            # не получилось/это таблица/код — режем по токенам
            atoms.extend(_slice_by_tokens(
                enc, b, max_tokens=max_tokens, overlap_tokens=overlap_tokens))
            continue

        # предложения тоже могут быть длинными (редко, но бывает) — подстрахуемся
        for s in sents:
            if _token_len(enc, s) <= max_tokens:
                atoms.append(s)
            else:
                atoms.extend(_slice_by_tokens(
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
        a_tok = _token_len(enc, a)
        # если текущий пуст — просто добавим
        if not cur_parts:
            cur_parts = [a]
            cur_tok = a_tok
            continue

        # проверяем, поместится ли (учитываем, что добавим еще "\n\n")
        sep_tok = _token_len(enc, "\n\n")
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
            if _token_len(enc, tail) >= min_tokens // 2:
                cur_parts = [tail, a]
                cur_tok = _token_len(enc, tail) + sep_tok + a_tok
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
        c_tok = _token_len(enc, c)
        if merged and c_tok < min_tokens:
            candidate = merged[-1] + "\n\n" + c
            if _token_len(enc, candidate) <= max_tokens:
                merged[-1] = candidate
                continue
        merged.append(c)

    return merged


def extract_text_from_pdf(pdf_file_path):
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


def extract_and_chunk(pdf_file_path):
    extracted_text = extract_text_from_pdf(pdf_file_path)
    chunks = chunk_text(extracted_text, target_tokens=350,
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
    return result_data
    # with open('data/rag_docs/output3.json', 'w', encoding='utf-8') as f:
    #     json.dump(result_data, f, ensure_ascii=False, indent=4)
