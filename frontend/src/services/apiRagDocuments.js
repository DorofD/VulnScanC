import { authFetch } from './authFetch';

export async function apiGetRagDocuments() {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/rag_documents`, { method: 'GET' })
    return response
}

export async function apiAddRagDocument(values) {
    // If caller passed a FormData (for file upload), send it directly without JSON headers
    if (values instanceof FormData) {
        // ensure action is included in FormData by caller
        const response = await authFetch(`${process.env.BACKEND_URL}/ai/rag_documents`, {
            method: 'POST',
            body: values
        })
        return response
    }

    const response = await authFetch(`${process.env.BACKEND_URL}/ai/rag_documents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'add', values: values })
    })
    return response
}

export async function apiChangeRagDocument(id, changes_dict) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/rag_documents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'change', id: id, fields_to_change: changes_dict })
    })
    return response
}

export async function apiDeleteRagDocument(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/rag_documents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'delete', id: id })
    })
    return response
}
