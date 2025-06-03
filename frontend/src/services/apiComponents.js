import { authFetch } from './authFetch';

export async function apiGetProjectComponents(project_id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/components?project_id=${project_id}`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiChangeComponentStatus(id, status) {
    const response = await authFetch(`${process.env.BACKEND_URL}/components`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'change',
            component_id: id,
            new_status: status
        })
    })
    return response
}

export async function apiAddProject(name) {
    const response = await authFetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add',
            name: name,
        })
    })
    return response
}
