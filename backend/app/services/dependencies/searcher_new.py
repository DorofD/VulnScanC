from __future__ import annotations
from pathlib import Path
import os
import hashlib
import base64
import requests
import time
import hashlib
from collections import defaultdict
from dataclasses import dataclass
import logging
import time
from typing import Any


# Если Hasher лежит в другом файле, например hasher.py:
# from hasher import Hasher, FileHash, DirectoryHash


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FileHash:
    path: str
    hash: str
    size: int


@dataclass(frozen=True)
class DirectoryHash:
    path: str
    hash: str
    file_count: int
    total_size: int


class Hasher:
    def __init__(self, extensions=None):
        self.extensions = extensions or {
            ".hpp", ".h", ".hh", ".cc", ".c", ".cpp"
        }

    # @staticmethod
    # def create_hash(file_path: Path) -> str:
    #     hash_obj = hashlib.sha256()

    #     with file_path.open("rb") as file:
    #         for chunk in iter(lambda: file.read(1024 * 1024), b""):
    #             hash_obj.update(chunk)

    #     return hash_obj.hexdigest()
    @staticmethod
    def create_hash(file_path: Path) -> str:
        hash_obj = hashlib.md5()

        with file_path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                hash_obj.update(chunk)

        return base64.b64encode(hash_obj.digest()).decode("utf-8")

    def should_scan_file(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.extensions

    def scan(self, root_dir: str) -> tuple[list[FileHash], list[DirectoryHash]]:
        root = Path(root_dir).resolve()

        file_hashes: list[FileHash] = []
        directory_items = defaultdict(list)

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if not self.should_scan_file(path):
                continue

            file_hash = self.create_hash(path)
            size = path.stat().st_size
            rel_path = path.relative_to(root).as_posix()

            file_hashes.append(
                FileHash(
                    path=rel_path,
                    hash=file_hash,
                    size=size,
                )
            )

            current_dir = path.parent

            while True:
                rel_to_current_dir = path.relative_to(current_dir).as_posix()

                directory_items[current_dir].append(
                    {
                        "relative_path": rel_to_current_dir,
                        "hash": file_hash,
                        "size": size,
                    }
                )

                if current_dir == root:
                    break

                current_dir = current_dir.parent

        directory_hashes: list[DirectoryHash] = []

        for directory, items in directory_items.items():
            dir_hash_obj = hashlib.sha256()

            total_size = 0

            for item in sorted(items, key=lambda x: x["relative_path"]):
                total_size += item["size"]

                line = (
                    item["relative_path"]
                    + "0"
                    + item["hash"]
                    + "0"
                    + str(item["size"])
                    + "\n"
                )

                dir_hash_obj.update(line.encode("utf-8"))

            directory_hashes.append(
                DirectoryHash(
                    path=directory.relative_to(root).as_posix()
                    if directory != root
                    else ".",
                    hash=dir_hash_obj.hexdigest(),
                    file_count=len(items),
                    total_size=total_size,
                )
            )

        return file_hashes, directory_hashes


class OsvSearcher:
    """Опрашивает OSV determineversion API на основании вывода Hasher.scan()."""

    API_URL = "https://api.osv.dev/v1experimental/determineversion"

    MAX_RETRIES = 5
    WAIT_TIME_BASE = 30
    REQUEST_DELAY = 0.1
    TIMEOUT = 60

    def __init__(
        self,
        api_url: str | None = None,
        max_retries: int | None = None,
        wait_time_base: int | None = None,
        request_delay: float | None = None,
        timeout: int | float | None = None,
        session: requests.Session | None = None,
    ):
        self.api_url = api_url or self.API_URL
        self.max_retries = max_retries if max_retries is not None else self.MAX_RETRIES
        self.wait_time_base = (
            wait_time_base if wait_time_base is not None else self.WAIT_TIME_BASE
        )
        self.request_delay = (
            request_delay if request_delay is not None else self.REQUEST_DELAY
        )
        self.timeout = timeout if timeout is not None else self.TIMEOUT
        self.session = session or requests.Session()

    def _send_request(self, data: dict[str, Any]) -> dict[str, Any]:
        """Отправляет запрос в OSV с retry на сетевые ошибки, 429 и 5xx."""

        time.sleep(self.request_delay)

        directory_name = data.get("name", "<unknown>")
        logger.info("OSV request for directory: %s", directory_name)
        # print("OSV request for directory: %s", directory_name)

        last_exc: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.post(
                    self.api_url,
                    json=data,
                    timeout=self.timeout,
                )

                if response.status_code == 429 or response.status_code >= 500:
                    raise requests.HTTPError(
                        f"OSV returned HTTP {response.status_code}: {response.text}",
                        response=response,
                    )

                response.raise_for_status()
                return response.json()

            except Exception as exc:
                last_exc = exc

                if attempt >= self.max_retries:
                    logger.error(
                        "OSV request failed after %s attempts. Directory: %s",
                        self.max_retries + 1,
                        directory_name,
                    )
                    raise

                wait_time = self.wait_time_base * (attempt + 1)

                logger.warning(
                    "OSV request failed. Directory: %s. "
                    "Attempt %s/%s. Waiting %s seconds. Error: %s",
                    directory_name,
                    attempt + 1,
                    self.max_retries + 1,
                    wait_time,
                    exc,
                )

                time.sleep(wait_time)

        # Теоретически сюда не дойдем, но для type-checker полезно.
        raise RuntimeError(f"OSV request failed: {last_exc}")

    @staticmethod
    def _best_match(matches: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Возвращает match с максимальным score."""

        if not matches:
            print('not mathec')
            return None

        return max(
            matches,
            key=lambda match: match.get("score", 0),
        )

    @staticmethod
    def _is_file_inside_directory(file_path: str, directory_path: str) -> bool:
        """Проверяет, лежит ли файл внутри директории.

        Пути ожидаются POSIX-style, например:

            src/lib/a.cpp
            src/lib
        """

        if directory_path == ".":
            return True

        prefix = directory_path.rstrip("/") + "/"
        return file_path.startswith(prefix)

    @staticmethod
    def _make_path_relative_to_directory(file_path: str, directory_path: str) -> str:
        """Делает путь файла относительным к директории.

        Пример:

            file_path:      src/lib/internal/a.cpp
            directory_path: src/lib

            result:         internal/a.cpp
        """

        if directory_path == ".":
            return file_path

        prefix = directory_path.rstrip("/") + "/"

        if not file_path.startswith(prefix):
            raise ValueError(
                f"File path {file_path!r} is not inside directory {directory_path!r}"
            )

        return file_path[len(prefix):]

    def _make_request_body_for_directory(
        self,
        directory: "DirectoryHash",
        file_hashes: list["FileHash"],
    ) -> dict[str, Any]:
        """Формирует тело запроса OSV для одной директории."""

        osv_file_hashes: list[dict[str, str]] = []

        for file_hash in file_hashes:
            if not self._is_file_inside_directory(file_hash.path, directory.path):
                continue

            relative_path = self._make_path_relative_to_directory(
                file_hash.path,
                directory.path,
            )

            osv_file_hashes.append(
                {
                    "file_path": relative_path,
                    "hash": file_hash.hash,
                }
            )

        return {
            "name": directory.path,
            "file_hashes": osv_file_hashes,
        }

    def _make_request_bodies(
        self,
        file_hashes: list["FileHash"],
        directory_hashes: list["DirectoryHash"],
    ) -> list[dict[str, Any]]:
        """Формирует список запросов в OSV для всех директорий."""

        bodies: list[dict[str, Any]] = []

        for directory in directory_hashes:
            body = self._make_request_body_for_directory(
                directory=directory,
                file_hashes=file_hashes,
            )

            if not body["file_hashes"]:
                continue

            bodies.append(body)

        return bodies

    def search_match(self, data: dict[str, Any]) -> dict[str, Any] | None:
        """Ищет лучший OSV match для одного тела запроса."""

        if not data.get("file_hashes"):
            return None

        response = self._send_request(data)

        matches = response.get("matches")
        if not matches:
            return None

        return self._best_match(matches)

    def search_all_matches(self, root_directory: str) -> list[dict[str, Any]]:
        """Сканирует директорию, отправляет данные в OSV и группирует лучшие совпадения.

        Возвращает список вида:

            [
                {
                    "repository": "https://github.com/...",
                    "directory": "vendor/some_lib",
                    "match": {...}
                }
            ]
        """

        hasher = Hasher()
        file_hashes, directory_hashes = hasher.scan(root_directory)

        bodies = self._make_request_bodies(
            file_hashes=file_hashes,
            directory_hashes=directory_hashes,
        )

        directory_matches: list[dict[str, Any]] = []

        for body in bodies:
            match = self.search_match(body)

            if not match:
                continue

            directory_matches.append(
                {
                    "directory": body["name"],
                    "match": match,
                }
            )

        return self._select_best_match_per_repository(directory_matches)

    def _select_best_match_per_repository(
        self,
        directory_matches: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Оставляет лучший match для каждого найденного репозитория."""

        best_by_repo: dict[str, dict[str, Any]] = {}

        for note in directory_matches:
            match = note["match"]
            repo_info = match.get("repo_info") or {}
            address = repo_info.get("address")

            if not address:
                continue

            current_best = best_by_repo.get(address)
            if current_best is None:
                best_by_repo[address] = note
                continue

            current_score = current_best["match"].get("score", 0)
            new_score = match.get("score", 0)

            if new_score > current_score:
                best_by_repo[address] = note

        result: list[dict[str, Any]] = []

        for address, note in best_by_repo.items():
            result.append(
                {
                    "repository": address,
                    "repo_info": note['repo_info'],
                    "directory": note["directory"],
                    "match": note["match"],
                }
            )

        result.sort(
            key=lambda item: item["match"].get("score", 0),
            reverse=True,
        )

        return result
