from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.routes import role_required
from app.services.api_services.ai import get_llama_hosts, add_llama_host, change_llama_host, delete_llama_host, send_messages


ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


@ai_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    print("Сhecking required services")
    llm_version = 'some_model'
    return jsonify({
        "llm_version": llm_version
    })


@ai_bp.route("/rag_chat/completions", methods=["POST"])
@jwt_required()
def completions():
    data = request.json
    print(data['messages'])
    messages = data['messages']
    response = send_messages(messages)
    if response:
        return jsonify(response)
    return jsonify({
        "success": True,
        "choices": [
            {
                "message":
                {
                    "role": 'assistant',
                    "content": "брат, саси)"
                }
            }
        ]
    })


@ai_bp.route("/llama_hosts", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def llama_hosts():
    if request.method == "GET":
        hosts = get_llama_hosts()
        return jsonify({"llama_hosts": hosts})
    if request.method == "POST":
        data = request.get_json()
        if data['action'] == 'add':
            result = add_llama_host(data['values'])
            return jsonify(result)
        if data['action'] == 'change':
            result = change_llama_host(
                data['id'], data.get('fields_to_change', {}))
            return jsonify(result)
        if data['action'] == 'delete':
            result = delete_llama_host(data['id'])
            return jsonify(result)


@ai_bp.route("/models/<string:model_id>", methods=["GET", "PATCH", "DELETE"])
@jwt_required()
@role_required("admin")
def model_item(model_id):
    if request.method == "GET":
        print(f"Get model config model_id={model_id}")
        return jsonify({"model_id": model_id})

    if request.method == "PATCH":
        data = request.get_json(silent=True) or {}
        print(f"Patch model config model_id={model_id}, data={data}")
        return jsonify({"success": True})

    print(f"Delete model config model_id={model_id}")
    return jsonify({"success": True})


@ai_bp.route("/models/<string:model_id>/test", methods=["POST"])
@jwt_required()
@role_required("admin")
def model_test(model_id):
    data = request.get_json(silent=True) or {}
    print(f"Test model model_id={model_id}, data={data}")
    return jsonify({"ok": True, "result": "..."})


@ai_bp.route("/model-presets", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def model_presets():
    if request.method == "GET":
        print("List model presets")
        return jsonify({"presets": []})

    data = request.get_json(silent=True) or {}
    print(f"Create model preset: {data}")
    return jsonify({"preset_id": "new_preset_id"}), 201


@ai_bp.route("/model-presets/<string:preset_id>", methods=["GET", "PATCH", "DELETE"])
@jwt_required()
@role_required("admin")
def model_preset_item(preset_id):
    if request.method == "GET":
        print(f"Get model preset preset_id={preset_id}")
        return jsonify({"preset_id": preset_id})

    if request.method == "PATCH":
        data = request.get_json(silent=True) or {}
        print(f"Patch model preset preset_id={preset_id}, data={data}")
        return jsonify({"success": True})

    print(f"Delete model preset preset_id={preset_id}")
    return jsonify({"success": True})


# -------------------------
# RAG ADMIN
# -------------------------

@ai_bp.route("/rag/collections", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def rag_collections():
    if request.method == "GET":
        print("List RAG collections")
        return jsonify({"collections": []})

    data = request.get_json(silent=True) or {}
    print(f"Create RAG collection: {data}")
    return jsonify({"collection_id": "new_collection_id"}), 201


@ai_bp.route("/rag/collections/<string:collection_id>", methods=["GET", "PATCH", "DELETE"])
@jwt_required()
@role_required("admin")
def rag_collection_item(collection_id):
    if request.method == "GET":
        print(f"Get RAG collection collection_id={collection_id}")
        return jsonify({"collection_id": collection_id})

    if request.method == "PATCH":
        data = request.get_json(silent=True) or {}
        print(
            f"Patch RAG collection collection_id={collection_id}, data={data}")
        return jsonify({"success": True})

    print(f"Delete RAG collection collection_id={collection_id}")
    return jsonify({"success": True})


@ai_bp.route("/rag/collections/<string:collection_id>/documents", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def rag_documents(collection_id):
    if request.method == "GET":
        print(f"List documents in collection_id={collection_id}")
        return jsonify({"documents": []})

    print(f"Upload/add document to collection_id={collection_id}")
    # тут может быть request.files или json с url
    return jsonify({"document_id": "new_document_id"}), 201


@ai_bp.route("/rag/documents/<string:document_id>", methods=["GET", "DELETE"])
@jwt_required()
@role_required("admin")
def rag_document_item(document_id):
    if request.method == "GET":
        print(f"Get document document_id={document_id}")
        return jsonify({"document_id": document_id})

    print(f"Delete document document_id={document_id}")
    return jsonify({"success": True})


@ai_bp.route("/rag/documents/<string:document_id>/chunks", methods=["GET"])
@jwt_required()
@role_required("admin")
def rag_document_chunks(document_id):
    print(f"List chunks document_id={document_id}")
    return jsonify({"chunks": []})


@ai_bp.route("/rag/documents/<string:document_id>/chunk", methods=["POST"])
@jwt_required()
@role_required("admin")
def rag_chunk_document(document_id):
    data = request.get_json(silent=True) or {}
    print(f"Run chunking document_id={document_id}, options={data}")
    return jsonify({"success": True})


@ai_bp.route("/rag/documents/<string:document_id>/embed", methods=["POST"])
@jwt_required()
@role_required("admin")
def rag_embed_document(document_id):
    data = request.get_json(silent=True) or {}
    print(f"Run embeddings document_id={document_id}, options={data}")
    return jsonify({"success": True})


@ai_bp.route("/rag/indexes", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def rag_indexes():
    if request.method == "GET":
        print("List RAG indexes")
        return jsonify({"indexes": []})

    data = request.get_json(silent=True) or {}
    print(f"Create RAG index: {data}")
    return jsonify({"index_id": "new_index_id"}), 201


@ai_bp.route("/rag/indexes/<string:index_id>", methods=["GET", "DELETE"])
@jwt_required()
@role_required("admin")
def rag_index_item(index_id):
    if request.method == "GET":
        print(f"Get RAG index index_id={index_id}")
        return jsonify({"index_id": index_id})

    print(f"Delete RAG index index_id={index_id}")
    return jsonify({"success": True})


@ai_bp.route("/rag/indexes/<string:index_id>/rebuild", methods=["POST"])
@jwt_required()
@role_required("admin")
def rag_index_rebuild(index_id):
    data = request.get_json(silent=True) or {}
    print(f"Rebuild index index_id={index_id}, options={data}")
    return jsonify({"success": True})


@ai_bp.route("/rag/search", methods=["POST"])
@jwt_required()
def rag_search():
    data = request.get_json(silent=True) or {}
    print(f"RAG search: {data}")
    return jsonify({"results": []})


@ai_bp.route("/rag/jobs", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def rag_jobs():
    if request.method == "GET":
        print("List RAG jobs")
        return jsonify({"jobs": []})

    data = request.get_json(silent=True) or {}
    print(f"Create RAG job: {data}")
    return jsonify({"job_id": "new_job_id"}), 201


@ai_bp.route("/rag/jobs/<string:job_id>", methods=["GET"])
@jwt_required()
@role_required("admin")
def rag_job_item(job_id):
    print(f"Get RAG job status job_id={job_id}")
    return jsonify({"job_id": job_id, "status": "running"})


@ai_bp.route("/rag/jobs/<string:job_id>/cancel", methods=["POST"])
@jwt_required()
@role_required("admin")
def rag_job_cancel(job_id):
    print(f"Cancel RAG job job_id={job_id}")
    return jsonify({"success": True})
