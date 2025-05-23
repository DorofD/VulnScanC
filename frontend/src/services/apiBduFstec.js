export async function apiGetBduInfo() {
    const response = await fetch(`${process.env.BACKEND_URL}/bdu?action=get_info`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiGetBduComponentVulns(component_id, component_type) {
    const response = await fetch(`${process.env.BACKEND_URL}/bdu?action=get_component_vulns&component_id=${component_id}&component_type=${component_type}`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiUpdateBdu() {
    const response = await fetch(`${process.env.BACKEND_URL}/bdu`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'update_bdu'
        })
    })
    return response
}

export async function apiUpdateBduVulns() {
    const response = await fetch(`${process.env.BACKEND_URL}/bdu`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'update_vulns'
        })
    })
    return response
}
