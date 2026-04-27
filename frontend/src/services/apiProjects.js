import { authFetch } from './authFetch';

export async function apiGetProjects() {
    const response = await authFetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiAddProject(name, description) {
    const response = await authFetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add',
            name: name,
            description: description,
        })
    })
    return response
}

export async function apiDeleteProject(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            id: id,
        })
    })
    return response
}

export async function apiChangeProject(id, name, description) {
    const response = await authFetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'change',
            id: id,
            name: name,
            description: description
        })
    })
    return response
}
