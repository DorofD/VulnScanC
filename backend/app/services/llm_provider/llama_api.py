import requests
import time
from typing import List, Optional
import requests


class Llama:
    def __init__(self):
        self.embed_url = "http://192.168.1.133:8081/v1/embeddings"
        # self.chat_url = "http://192.168.1.133:8080/v1/chat/completions"
        self.chat_url = "http://192.168.5.226:8080/v1/chat/completions"

    def get_embedding(self, text: str, retries: int = 3, sleep_s: float = 1.0) -> List[float]:
        """
        Дергает llama.cpp embeddings endpoint и возвращает вектор (list[float])
        """
        payload = {"input": text}
        last_err: Optional[Exception] = None

        for _ in range(retries):
            try:
                r = requests.post(
                    self.embed_url, json=payload, timeout=840)
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
                     model: str = "local"):
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
            r = requests.post(self.chat_url, json=payload,
                              headers=headers, timeout=840)
            r.raise_for_status()
            data = r.json()
            return data
        except Exception as exc:
            print('Error:', exc)
