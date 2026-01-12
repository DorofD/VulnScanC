
from app.adapters.llama_api import LlamaApiAdapter
from app.pg_repository.queries.llama_nodes import DBLlamaChatNodes, DBLlamaEmbeddingNodes


def get_llama_nodes_summary():
    """Collect `/v1/models` info from all chat and embedding nodes.

    Returns: {"chat_nodes": [...], "embedding_nodes": [...]} where each item is the
    original node record extended with a `models` key containing the result of
    `Llama.get_node_info` or `{'success': False}` on error.
    """
    chat_nodes = DBLlamaChatNodes().get_nodes()
    embedding_nodes = DBLlamaEmbeddingNodes().get_nodes()

    def enrich(nodes, llama):
        out = []
        for n in nodes or []:
            base = n.get('base_api_url')
            info = LlamaApiAdapter(base).get_node_info()
            item = dict(n)
            item['models'] = info
            out.append(item)
        return out

    return {"chat_nodes": enrich(chat_nodes), "embedding_nodes": enrich(embedding_nodes)}


def get_llama_nodes():
    # legacy combined listing: return both arrays
    chat = DBLlamaChatNodes().get_nodes()
    embedding = DBLlamaEmbeddingNodes().get_nodes()
    return {"chat_nodes": chat, "embedding_nodes": embedding}


def get_llama_chat_nodes():
    return DBLlamaChatNodes().get_nodes()


def get_llama_embedding_nodes():
    return DBLlamaEmbeddingNodes().get_nodes()


def get_embedding_base_api_url() -> str:
    """Return base_api_url from any embedding node (first available).

    Raises RuntimeError if no embedding nodes are configured.
    """
    nodes = DBLlamaEmbeddingNodes().get_nodes()
    if not nodes:
        raise RuntimeError(
            "No embedding nodes configured in llama_embedding_nodes")
    # pick the first configured embedding node
    node = nodes[0]
    return node.get('base_api_url')


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
