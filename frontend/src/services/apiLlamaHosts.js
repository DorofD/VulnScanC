import { authFetch } from './authFetch';

export async function apiGetLlamaHosts() {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_hosts`, {
        method: 'GET',
    })
    return response
}

export async function apiAddLlamaHost(values) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_hosts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add',
            values: values
        })
    })
    return response
}

export async function apiChangeLlamaHost(id, changes_dict) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_hosts`, {
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

export async function apiDeleteLlamaHost(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/ai/llama_hosts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            id: id
        })
    })
    return response
}
