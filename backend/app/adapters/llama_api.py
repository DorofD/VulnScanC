import requests
import time
from typing import List, Optional
import requests


class LlamaApiAdapter:
    def __init__(self, base_api_url):
        if not base_api_url:
            raise RuntimeError('No base_api_url provided for chat')
        self.base_url = base_api_url

    def get_node_info(self):
        target = self.base_url.rstrip('/') + '/v1/models'
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


class LlamaChatApiAdapter(LlamaApiAdapter):

    def send_message(self,
                     messages: list = [],
                     temperature: float = 0.2,
                     max_tokens: int = 300,
                     stream: bool = False,
                     model: str = "local"):
        target_url = self.base_url.rstrip('/') + '/v1/chat/completions'
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

    def get_node_info(self):
        target = self.base_url.rstrip('/') + '/v1/models'
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


class LlamaEmbeddingApiAdapter(LlamaApiAdapter):

    def get_embedding_dimension(self):
        """Получить размерность эмбеддинга"""
        dim = len(self.get_embedding(
            "dimension check", self.base_url))
        return dim

    def get_embedding(self, text: str, retries: int = 3, sleep_s: float = 1.0) -> List[float]:
        """
        Дергает llama.cpp embeddings endpoint и возвращает вектор (list[float])
        """
        payload = {"input": text}
        last_err: Optional[Exception] = None

        for _ in range(retries):
            try:
                target = self.base_url.rstrip('/') + '/v1/embeddings'
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
