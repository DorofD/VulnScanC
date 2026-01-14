import re
import tiktoken
from typing import List


class Chunker:
    """
    Утилита для разбиения длинных текстов на чанки, подходящие для контекста LLM
    с ограничением по количеству токенов.

    Класс старается формировать чанки, близкие к `target_tokens`, не превышая
    `max_tokens`, и избегать очень маленьких фрагментов (меньше `min_tokens`).

    Краткая стратегия:
    - Грубое разбиение по пустым строкам / разделам (markdown-подобно).
    - Для больших блоков — попытка разбить по предложениям.
    - Если предложения всё ещё слишком длинные — разбиение по токенам.
    - В конце объединение «атомов» в чанки с опциональным overlap.
    """

    def __init__(self):
        # Регулярное выражение для разбиения на предложения. Пытаемся разделить
        # после обычных терминаторов предложений, за которыми следует пробел и
        # заглавная буква или цифра (поддерживает латиницу и кириллицу).
        # Выражение простое — идеальная сегментация предложений не обязательна
        # для логики чанкинга.
        self.sent_split = re.compile(r"(?<=[.!?…])s+(?=[A-ZА-ЯЁ0-9])")

    def _split_by_regex(self, text: str, pattern: re.Pattern) -> List[str]:
        """Разбить `text` с помощью `pattern`, вернуть непустые, обрезанные части.

        Тонкая оболочка над `re.split` — нормализует пробелы и отбрасывает пустые
        фрагменты. Используется в основном для разбиения блока на предложения.
        """
        parts = pattern.split(text)
        return [p.strip() for p in parts if p and p.strip()]

    def _token_len(self, enc, s: str) -> int:
        """Вернуть число токенов для строки `s` с энкодером `enc`.

        Небольшая обёртка, чтобы все проверки длины в токенах использовали один
        и тот же экземпляр энкодера.
        """
        return len(enc.encode(s))

    def _slice_by_tokens(self, enc, text: str, max_tokens: int, overlap_tokens: int = 0) -> List[str]:
        """Разбить `text` на куски, ограниченные по числу токенов.

        - Кодируем весь `text` в токен-ids и идём по ним шагами.
        - `step` равен `max_tokens - overlap_tokens`, чтобы при необходимости
            сохранять overlap между соседними чанками (полезно для непрерывности
            контекста).
        - Каждая часть декодируется обратно в текст и обрезается.

        Это запасной вариант, когда ни разделение на блоки, ни на предложения
        не даёт достаточно маленьких «атомов».
        """
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
        max_tokens: int = 330,        # жесткий потолок
        min_tokens: int = 80,        # чтобы не плодить мусор
        overlap_tokens: int = 20,
        encoding_name: str = "cl100k_base",
    ) -> List[str]:

        enc = tiktoken.get_encoding(encoding_name)
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
                # соединяем части пустой строкой, чтобы сохранить параграфную
                # структуру при объединении обратно в чанк
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
