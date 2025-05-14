export async function apiGetBitbakeProjects() {
    const response = await fetch(`${process.env.BACKEND_URL}/bitbake?action=get_projects`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiAddBitbakeProject(name) {
    const response = await fetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add_project',
            project_name: name,
        })
    })
    return response
}

export async function apiDeleteBitbakeProject(id) {
    const response = await fetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete_project',
            project_id: id,
        })
    })
    return response
}

export async function apiChangeBitbakeProject(id, name) {
    const response = await fetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'change_project',
            project_id: id,
            project_name: name
        })
    })
    return response
}

export async function apiGetBitbakeProjectComponents(project_id, layer) {
    const response = await fetch(`${process.env.BACKEND_URL}/bitbake?action=get_components&project_id=${project_id}&layer=${layer}`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiGetBitbakeComponentVulnerabilities(component_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/bitbake?action=get_vulnerabilities&component_id=${component_id}`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}
