from app.pg_repository.queries.rag_documents import DBRagDocuments
from app.pg_repository.queries.rag_chunks import DBRagChunks
from app.pg_repository.queries.llama_nodes import DBLlamaEmbeddingNodes
from app.adapters.pdf_extract import PDFExtractAdapter
from app.adapters.llama_api import LlamaEmbeddingApiAdapter
from app.adapters.chunker import Chunker
import os
import logging
import json


def get_rag_documents():
    docs = DBRagDocuments().get_documents()
    for doc in docs:
        file_size = os.path.getsize(doc['file_path'])
        file_size_mb = file_size / (1024 * 1024)
        file_size_str = f"{file_size_mb:.4f} МБ"
        doc['file_size'] = file_size_str

    return docs


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
    description = fields_to_update.get(
        'description', existing.get('description'))

    DBRagDocuments().update_document(id, name, file_path, description)
    return True


def delete_rag_document(id: int):
    # Получаем запись перед удалением, чтобы узнать путь к файлу
    existing = DBRagDocuments().get_document(id)
    if not existing:
        raise Exception(f'rag_document with id {id} not found')

    file_path = existing.get('file_path')
    if file_path:
        try:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logging.exception(
                f"Failed to remove file for rag_document {id}: {file_path}")

    return DBRagDocuments().delete_document(id)


def cut_document_to_chunks(id):
    doc_note = DBRagDocuments().get_document(id)
    if not doc_note:
        raise Exception(f'rag_document with id {id} not found')
    pdf_ex = PDFExtractAdapter()
    full_text = pdf_ex.extract_text(doc_note['file_path'])
    chunker = Chunker()
    chunks = chunker.chunk_text(full_text)
    print(len(chunks))
    data = [{'raw_text': txt} for txt in chunks]

    file_to_save = os.path.join(
        'data', 'rag_docs', f"{doc_note['uuid']}_chunks.json")
    with open(file_to_save, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def calculate_embeddings_for_document(id):
    pg_rag = DBRagChunks()
    doc_note = DBRagDocuments().get_document(id)
    if not doc_note:
        raise Exception(f'rag_document with id {id} not found')
    saved_json = os.path.join(
        'data', 'rag_docs', f"{doc_note['uuid']}_chunks.json")
    with open(saved_json, 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    pg_embedding = DBLlamaEmbeddingNodes()
    node = pg_embedding.get_nodes()
    if not node:
        raise RuntimeError('No embedding nodes configured')
    base_api_url = node[0]['base_api_url']
    llama_embed = LlamaEmbeddingApiAdapter(base_api_url)
    count = 0
    for ch in chunks:
        count += 1
        raw_text = ch["raw_text"]
        emb = llama_embed.get_embedding(raw_text)

        print('NUMBER', count)
        pg_rag.upsert_chunk(
            document_id=id,
            raw_text=raw_text,
            embedding=emb
        )
        print('NUMBER', count, 'DONE')
