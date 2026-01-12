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
                if not base_api_url:
                    raise RuntimeError(
                        'No base_api_url provided for embeddings')
                target = base_api_url.rstrip('/') + '/v1/embeddings'
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
        if not base_api_url:
            raise RuntimeError('No base_api_url provided for chat')
        target_url = base_api_url.rstrip('/') + '/v1/chat/completions'
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

    def get_node_info(self, base_api_url: str = None):
        """Fetch node info from the model node at /v1/models.

        Returns the `models` object on success or {'success': False} on any error.
        """
        if not base_api_url:
            return {'success': False}
        target = base_api_url.rstrip('/') + '/v1/models'
        try:
            r = requests.get(target, timeout=30)
            r.raise_for_status()
            data = r.json()
            models = data.get('models')
            if models is None:
                return {'success': False}
            return {'success': True, 'models': models}
        except Exception as exc:
            print(exc)
            return {'success': False}
