import json
import os
from datetime import datetime

from app.services.osv_scanner.osv_scanner import OSVScanner
from app.services.search_data.search_data import SearchDataService


class SaveHashesService:
    def __init__(self):
        self.osv_scanner = OSVScanner()
        self.search_data_service = SearchDataService()
        self.hashes_dir = 'data/hashes'

    def save_hashes(self, data: dict) -> str:
        """
        Сохраняет хеши в JSON-файл и запускает OSV-сканирование.

        data: {
            "project_name": "...",
            "datetime": "dd_mm_yyyy_hh_mm",
            "hashes": [...]
        }

        Возвращает путь к сохранённому файлу.
        """
        project_name = data['project_name']
        datetime_str = data['datetime']
        hashes = data['hashes']

        os.makedirs(self.hashes_dir, exist_ok=True)

        filename = f'{project_name}_{datetime_str}_hashes.json'
        filepath = os.path.join(self.hashes_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        matches_with_vulns = self.osv_scanner.process_hashes(hashes)

        handled_data = self._build_handled_data(matches_with_vulns)

        self.search_data_service.save_search_data({
            'status': 'ok',
            'project_name': project_name,
            'datetime': datetime_str,
            'dependencies': handled_data,
            'vulnerabilities': []
        })

        return filepath

    def save_hashes_only(self, data: dict) -> str:
        """
        Сохраняет хеши в JSON-файл без OSV-сканирования.
        Используется для отложенной обработки через очереди.

        Возвращает путь к сохранённому файлу.
        """
        project_name = data['project_name']
        datetime_str = data['datetime']
        hashes = data['hashes']

        os.makedirs(self.hashes_dir, exist_ok=True)

        filename = f'{project_name}_{datetime_str}_hashes.json'
        filepath = os.path.join(self.hashes_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return filepath

    def trigger_scan(self, project_name: str, datetime_str: str) -> bool:
        """
        Загружает сохранённый JSON хешей и запускает OSV-сканирование.
        Используется для отложенной обработки (очереди Redis).
        """
        filename = f'{project_name}_{datetime_str}_hashes.json'
        filepath = os.path.join(self.hashes_dir, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Hashes file not found: {filepath}")

        with open(filepath, 'r') as f:
            data = json.load(f)

        hashes = data['hashes']

        matches_with_vulns = self.osv_scanner.process_hashes(hashes)
        handled_data = self._build_handled_data(matches_with_vulns)

        self.search_data_service.save_search_data({
            'status': 'ok',
            'project_name': project_name,
            'datetime': datetime_str,
            'dependencies': handled_data,
            'vulnerabilities': []
        })

        return True

    def _build_handled_data(self, matches_with_vulns: list) -> list:
        """
        Преобразует результат OSVScanner в формат, ожидаемый SearchDataService.
        SearchDataService._handle_data ожидает список зависимостей,
        где каждая зависимость — dict с полями 'directory' и 'vulnerabilities'.
        """
        handled_data = []
        for match in matches_with_vulns:
            entry = {
                'directory': match['directory'],
                'match': match['match']
            }
            if 'vulns' in match:
                entry['vulnerabilities'] = match['vulns']
            handled_data.append(entry)
        return handled_data
