import { authFetch } from './authFetch';

export async function apiRagChatGetInfo() {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai_chat`, {
        method: 'GET',
    })
    return response
}

export async function apiRagChatSendMessage(messages, modelUuid) {
    const body = { messages: messages };
    if (modelUuid) body.model_uuid = modelUuid;

    const response = await authFetch(`${process.env.BACKEND_URL}/ai/rag_chat/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    return response
}

export async function apiChangeUser(id, changes_dict) {
    const response = await authFetch(`${process.env.BACKEND_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'change',
            id: id,
            fields_to_change: changes_dict
        })
    })
    return response
}

export async function apiDeleteUser(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            id: id
        })
    })
    return response
}