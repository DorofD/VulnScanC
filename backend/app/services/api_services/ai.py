from app.services.llm_provider.llama_api import Llama
from app.services.llm_provider.chunk_handler import ChunkHandler
from app.pg_repository.queries.llama_nodes import DBLlamaChatNodes, DBLlamaEmbeddingNodes


def send_messages(messages, model_uuid: str = None):
    msg_count = len(messages)
    # print(messages)

    llama = Llama()
    ch = ChunkHandler()
    host_info = None
    if model_uuid:
        # search in chat nodes first
        host_info = DBLlamaChatNodes().get_node_by_uuid(model_uuid)
        if not host_info:
            # fall back to embedding nodes lookup (in case uuid provided for embedding)
            host_info = DBLlamaEmbeddingNodes().get_node_by_uuid(model_uuid)
        if not host_info:
            return {"error": "model not found", "status": 400}
    if msg_count == 1:
        user_text = messages[0]['content']
        topk_chunks = ch.search_topk(user_text, k=5)

        for i in topk_chunks:
            print(i['chunk_number'], i['cosine_similarity'])

        system_prompt_str = "Ты специалист по ИБ, отвечай строго на основе CONTEXT, если в CONTEXT нет ответа - так и скажи"
        context_str = ch.build_context_content(topk_chunks)

        final_messages = [
            {"role": "system", "content": system_prompt_str},
            {"role": "user", "content": context_str},
            {"role": "user", "content": user_text}

        ]
        base = host_info['base_api_url'] if host_info else None
        response = llama.send_message(final_messages, base_api_url=base)
        if response:
            return response
        return False
    return False


def get_llama_nodes():
    # legacy combined listing: return both arrays
    chat = DBLlamaChatNodes().get_nodes()
    embedding = DBLlamaEmbeddingNodes().get_nodes()
    return {"chat_nodes": chat, "embedding_nodes": embedding}


def get_llama_chat_nodes():
    return DBLlamaChatNodes().get_nodes()


def get_llama_embedding_nodes():
    return DBLlamaEmbeddingNodes().get_nodes()


def add_llama_chat_node(values):
    base_api_url = values.get('base_api_url') or values.get('api_url')
    try:
        name = values['name']
    except KeyError:
        name = ''
    try:
        description = values['description']
    except KeyError:
        description = ''
    result = DBLlamaChatNodes().add_node(base_api_url, name, description)
    print(result)
    return result


def add_llama_embedding_node(values):
    base_api_url = values.get('base_api_url') or values.get('api_url')
    try:
        name = values['name']
    except KeyError:
        name = ''
    try:
        description = values['description']
    except KeyError:
        description = ''
    result = DBLlamaEmbeddingNodes().add_node(base_api_url, name, description)
    print(result)
    return result


def change_llama_chat_node(id, fields_to_change: dict):
    db = DBLlamaChatNodes()
    last = None
    for field, value in fields_to_change.items():
        last = db.update_node_field(id, field, value)
    return last


def change_llama_embedding_node(id, fields_to_change: dict):
    db = DBLlamaEmbeddingNodes()
    last = None
    for field, value in fields_to_change.items():
        last = db.update_node_field(id, field, value)
    return last


def delete_llama_chat_node(id):
    result = DBLlamaChatNodes().delete_node(id)
    return result


def delete_llama_embedding_node(id):
    result = DBLlamaEmbeddingNodes().delete_node(id)
    return result


def move_node_between_tables(id: int, from_type: str, to_type: str):
    # from_type/to_type should be 'chat' or 'embedding'
    if from_type == to_type:
        return None
    if from_type == 'chat':
        src = DBLlamaChatNodes()
        dst = DBLlamaEmbeddingNodes()
    else:
        src = DBLlamaEmbeddingNodes()
        dst = DBLlamaChatNodes()

    record = src.get_node_by_id(id)
    if not record:
        return {"error": "not found", "status": 404}

    # insert into destination
    new = dst.add_node(record['base_api_url'], record.get(
        'name', ''), record.get('description', ''))
    # delete old
    src.delete_node(id)
    return new
