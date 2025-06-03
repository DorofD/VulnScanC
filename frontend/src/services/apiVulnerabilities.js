import { authFetch } from './authFetch';

export async function apiGetComponentVulnerabilities(component_id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/vulnerabilities?component_id=${component_id}`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}
