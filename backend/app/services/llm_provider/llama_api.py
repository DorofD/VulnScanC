import os
import requests
import time
from typing import List, Optional
import requests


class Llama:
    def __init__(self):
        pass

    def get_embedding(self, text: str, retries: int = 3, sleep_s: float = 1.0, base_api_url: str = None) -> List[float]:
        """
        Дергает llama.cpp embeddings endpoint и возвращает вектор (list[float])
        """
        payload = {"input": text}
        last_err: Optional[Exception] = None

        for _ in range(retries):
            try:
                base = base_api_url or getattr(
                    self, 'embed_url', None) or os.environ.get('LLAMA_BASE_API_URL')
                if not base:
                    raise RuntimeError(
                        'No base_api_url provided for embeddings')
                target = base.rstrip('/') + '/v1/embeddings'
                r = requests.post(target, json=payload, timeout=840)
                r.raise_for_status()
                data = r.json()
                # Ожидаем формат: {"data":[{"embedding":[...]}], ...}
                return data["data"][0]["embedding"]
            except Exception as e:
                last_err = e
                time.sleep(sleep_s)
        raise RuntimeError(
            f"Failed to get embedding after {retries} retries: {last_err}")

    def send_message(self,
                     messages: list = [],
                     temperature: float = 0.2,
                     max_tokens: int = 300,
                     stream: bool = False,
                     model: str = "local",
                     base_api_url: str = None):
        base = base_api_url or getattr(
            self, 'chat_url', None) or os.environ.get('LLAMA_BASE_API_URL')
        if not base:
            raise RuntimeError('No base_api_url provided for chat')
        target_url = base.rstrip('/') + '/v1/chat/completions'
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            "model": model
        }
        headers = {
            'Content-Type': 'application/json',
        }
        try:
            r = requests.post(target_url, json=payload,
                              headers=headers, timeout=840)
            r.raise_for_status()
            data = r.json()
            return data
        except Exception as exc:
            print('Error:', exc)
