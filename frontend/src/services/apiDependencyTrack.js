import { authFetch } from './authFetch';
export async function apiGetProjects() {
    const response = await authFetch(`${process.env.BACKEND_URL}/dependency_track?action=get_projects`, {
        method: 'GET',
    })
    const projects = await response.json()
    if (response.status === 500) {
        throw new Error('Internal Server Error.');
    }
    return projects
}

export async function apiGetComponents(project_uuid) {
    const response = await authFetch(`${process.env.BACKEND_URL}/dependency_track?action=get_components&project_uuid=${project_uuid}`, {
        method: 'GET',
    })
    const projects = await response.json()
    if (response.status === 500) {
        throw new Error('Internal Server Error.');
    }
    return projects
}

