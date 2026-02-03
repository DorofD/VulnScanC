from app.pg_repository.queries.rag_documents import DBRagDocuments
import os
import logging


def get_rag_documents():
    docs = DBRagDocuments().get_documents()
    for doc in docs:
        file_size = os.path.getsize(doc['file_path'])
        file_size_mb = file_size / (1024 * 1024)
        file_size_str = f"{file_size_mb:.4f} МБ"
        doc['file_size'] = file_size_str

    return docs


def get_rag_document(id: int):
    return DBRagDocuments().get_document(id)


def add_rag_document(name: str, description: str = None):
    if not name:
        raise Exception(
            'name and file_path are required to add a rag_document')
    return DBRagDocuments().add_document(name, description)


def change_rag_document(id: int, fields_to_update: dict):
    existing = DBRagDocuments().get_document(id)
    if not existing:
        raise Exception(f'rag_document with id {id} not found')

    name = fields_to_update.get('name', existing.get('name'))
    file_path = fields_to_update.get('file_path', existing.get('file_path'))

    DBRagDocuments().update_document(id, name, file_path)
    return True


def delete_rag_document(id: int):
    # Получаем запись перед удалением, чтобы узнать путь к файлу
    existing = DBRagDocuments().get_document(id)
    if not existing:
        raise Exception(f'rag_document with id {id} not found')

    file_path = existing.get('file_path')
    if file_path:
        try:
            # Удаляем файл, если он существует
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            # Логируем ошибку, но не прерываем удаление записи в БД
            logging.exception(
                f"Failed to remove file for rag_document {id}: {file_path}")

    return DBRagDocuments().delete_document(id)
