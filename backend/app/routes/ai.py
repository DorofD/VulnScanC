from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.routes import role_required
from app.services.api_services.ai import (
    get_llama_nodes,
    get_llama_chat_nodes,
    get_llama_embedding_nodes,
    get_llama_nodes_summary,
    add_llama_chat_node,
    add_llama_embedding_node,
    change_llama_chat_node,
    change_llama_embedding_node,
    delete_llama_chat_node,
    delete_llama_embedding_node,
    move_node_between_tables,
    send_messages,
)
from app.services.rag_documents import (
    get_rag_documents,
    add_rag_document,
    change_rag_document,
    delete_rag_document,
)


ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


@ai_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    # return aggregated node model info
    data = get_llama_nodes_summary()
    return jsonify(data)


@ai_bp.route("/rag_chat/completions", methods=["POST"])
@jwt_required()
def completions():
    data = request.json
    print(data['messages'])
    messages = data['messages']
    model_uuid = data.get('model_uuid')
    response = send_messages(messages, model_uuid=model_uuid)
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


@ai_bp.route("/llama_nodes", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def llama_nodes():
    if request.method == "GET":
        hosts = get_llama_nodes()
        # return combined structure for backward compatibility
        return jsonify(hosts)
    if request.method == "POST":
        data = request.get_json()
        # Legacy POST: route based on provided model_type (if any)
        if data['action'] == 'add':
            vals = data.get('values', {})
            mtype = vals.get('model_type')
            if mtype == 'embedding':
                result = add_llama_embedding_node(vals)
            else:
                # default to chat
                result = add_llama_chat_node(vals)
            return jsonify(result)
        if data['action'] == 'change':
            # require explicit table selection via 'node_type' in payload
            node_type = data.get('node_type')
            fields = data.get('fields_to_change', {})
            # if model_type change requested — move between tables
            if 'model_type' in fields and fields['model_type'] != node_type:
                # perform move
                new = move_node_between_tables(
                    data['id'], node_type, fields['model_type'])
                return jsonify(new)
            if node_type == 'embedding':
                result = change_llama_embedding_node(
                    data['id'], data.get('fields_to_change', {}))
            else:
                result = change_llama_chat_node(
                    data['id'], data.get('fields_to_change', {}))
            return jsonify(result)
        if data['action'] == 'delete':
            node_type = data.get('node_type')
            if node_type == 'embedding':
                result = delete_llama_embedding_node(data['id'])
            else:
                result = delete_llama_chat_node(data['id'])
            return jsonify(result)


@ai_bp.route("/llama_chat_nodes", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def llama_chat_nodes():
    if request.method == "GET":
        nodes = get_llama_chat_nodes()
        return jsonify({"chat_nodes": nodes})
    if request.method == "POST":
        data = request.get_json()
        if data['action'] == 'add':
            result = add_llama_chat_node(data.get('values', {}))
            return jsonify(result)
        if data['action'] == 'change':
            result = change_llama_chat_node(
                data['id'], data.get('fields_to_change', {}))
            return jsonify(result)
        if data['action'] == 'delete':
            result = delete_llama_chat_node(data['id'])
            return jsonify(result)


@ai_bp.route("/llama_embedding_nodes", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def llama_embedding_nodes():
    if request.method == "GET":
        nodes = get_llama_embedding_nodes()
        return jsonify({"embedding_nodes": nodes})
    if request.method == "POST":
        data = request.get_json()
        if data['action'] == 'add':
            result = add_llama_embedding_node(data.get('values', {}))
            return jsonify(result)
        if data['action'] == 'change':
            result = change_llama_embedding_node(
                data['id'], data.get('fields_to_change', {}))
            return jsonify(result)
        if data['action'] == 'delete':
            result = delete_llama_embedding_node(data['id'])
            return jsonify(result)


@ai_bp.route("/rag_documents", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def rag_documents():
    if request.method == "GET":
        nodes = get_rag_documents()
        return jsonify({"rag_documents": nodes})
    if request.method == "POST":
        data = request.get_json()
        if data['action'] == 'add':
            result = add_rag_document(data.get('values', {}))
            return jsonify(result)
        if data['action'] == 'change':
            result = change_rag_document(
                data['id'], data.get('fields_to_change', {}))
            return jsonify(result)
        if data['action'] == 'delete':
            result = delete_rag_document(data['id'])
            return jsonify(result)
