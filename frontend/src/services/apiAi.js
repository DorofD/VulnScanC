import { authFetch } from './authFetch';

export async function apiChatGetInfo() {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai_chat`, {
        method: 'GET',
    })
    return response
}

export async function apiAiChatSendMessage(messages, useRag) {
    const body = { messages: messages };
    body.use_rag = useRag;
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    return response
}

export async function apiAiChatSendMessage1(messages, useRag) {
    const body = { messages: messages };
    body.use_rag = useRag;
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    return response
}
