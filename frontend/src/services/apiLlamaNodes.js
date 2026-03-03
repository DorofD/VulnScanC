import { authFetch } from './authFetch';

export async function apiGetLlamaNodes() {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_nodes`, {
        method: 'GET',
    })
    return response
}

export async function apiAddLlamaNode(values) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add',
            values: values
        })
    })
    return response
}

export async function apiChangeLlamaNode(id, changes_dict, node_type = null) {
    const body = {
        action: 'change',
        id: id,
        fields_to_change: changes_dict
    }
    if (node_type) body.node_type = node_type
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    return response
}

export async function apiDeleteLlamaNode(id, node_type = null) {
    const body = { action: 'delete', id: id }
    if (node_type) body.node_type = node_type
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    return response
}
export async function apiSetActiveLlamaNode(node_uuid, node_type ) {
    const body = { action: 'set_active', node_uuid: node_uuid, node_type: node_type }
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    return response
}

// New: explicit endpoints for chat and embedding nodes
export async function apiGetChatNodes() {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_chat_nodes`, { method: 'GET' })
    return response
}

export async function apiGetEmbeddingNodes() {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_embedding_nodes`, { method: 'GET' })
    return response
}

export async function apiAddChatNode(values) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_chat_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'add', values: values })
    })
    return response
}

export async function apiAddEmbeddingNode(values) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_embedding_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'add', values: values })
    })
    return response
}

export async function apiChangeChatNode(id, changes_dict) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_chat_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'change', id: id, fields_to_change: changes_dict })
    })
    return response
}

export async function apiChangeEmbeddingNode(id, changes_dict) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_embedding_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'change', id: id, fields_to_change: changes_dict })
    })
    return response
}

export async function apiDeleteChatNode(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_chat_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'delete', id: id })
    })
    return response
}

export async function apiDeleteEmbeddingNode(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_embedding_nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'delete', id: id })
    })
    return response
}
