from app.pg_repository.queries.rag_documents import DBRagDocuments


def get_rag_documents():
    return DBRagDocuments().get_documents()


def get_rag_document(id: int):
    return DBRagDocuments().get_document(id)


def add_rag_document(values: dict):
    name = values.get('name')
    file_path = values.get('file_path')
    if not name or not file_path:
        raise Exception(
            'name and file_path are required to add a rag_document')
    return DBRagDocuments().add_document(name, file_path)


def change_rag_document(id: int, fields_to_update: dict):
    existing = DBRagDocuments().get_document(id)
    if not existing:
        raise Exception(f'rag_document with id {id} not found')

    name = fields_to_update.get('name', existing.get('name'))
    file_path = fields_to_update.get('file_path', existing.get('file_path'))

    DBRagDocuments().update_document(id, name, file_path)
    return True


def delete_rag_document(id: int):
    return DBRagDocuments().delete_document(id)
