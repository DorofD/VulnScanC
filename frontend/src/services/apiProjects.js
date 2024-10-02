export async function apiGetProjects() {
    const response = await fetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiAddProject(name) {
    const response = await fetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add',
            name: name,
        })
    })
    return response
}

export async function apiDeleteProject(id) {
    const response = await fetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            project_id: id,
        })
    })
    return response
}

export async function apiChangeProject(id, name) {
    const response = await fetch(`${process.env.BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'change',
            project_id: id,
            project_name: name
        })
    })
    return response
}