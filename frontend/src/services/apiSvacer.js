export async function apiGetSvacerProjects() {
    const response = await fetch(`${process.env.BACKEND_URL}/svacer?action=get_projects`, {
        method: 'GET',
    })
    const projects = await response.json()
    if (response.status === 500) {
        throw new Error('Internal Server Error.');
    }
    return projects
}

export async function apiGetSvacerSnapshots(project_id, branch_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/svacer?action=get_snapshots&project_id=${project_id}&branch_id=${branch_id}`, {
        method: 'GET',
    })
    const projects = await response.json()
    if (response.status === 500) {
        throw new Error('Internal Server Error.');
    }
    return projects
}

