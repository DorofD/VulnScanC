from app.services.llm_provider.llama_api import Llama
from app.services.llm_provider.chunk_handler import ChunkHandler
from app.pg_repository.queries.llama_hosts import DBLlamaHosts


def send_messages(messages):
    msg_count = len(messages)
    # print(messages)

    llama = Llama()
    ch = ChunkHandler()
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
        response = llama.send_message(final_messages)
        if response:
            return response
        return False
    return False


def get_llama_hosts():
    result = DBLlamaHosts().get_hosts()
    return result


def add_llama_host(values):
    api_url = values['api_url']
    model_type = values['model_type']
    try:
        name = values['name']
    except KeyError:
        name = ''
    try:
        description = values['description']
    except KeyError:
        description = ''
    result = DBLlamaHosts().add_host(api_url, model_type, name, description)
    print(result)
    return result


def change_llama_host(id, fields_to_change: dict):
    # fields_to_change is a dict of field -> value; update each field
    db = DBLlamaHosts()
    last = None
    for field, value in fields_to_change.items():
        last = db.update_host_field(id, field, value)
    return last


def delete_llama_host(id):
    result = DBLlamaHosts().delete_host(id)
    return result
