import { authFetch } from './authFetch';

export async function apiGetBitbakeProjects() {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake?action=get_projects`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiAddBitbakeProject(name) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add_project',
            project_name: name,
        })
    })
    return response
}

export async function apiAddBitbakeLicense(component_id, license_name, recipe_name) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add_license',
            component_id: component_id,
            license_name: license_name,
            recipe_name: recipe_name,
        })
    })
    return response
}

export async function apiDeleteBitbakeProject(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
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
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
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
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake?action=get_components&project_id=${project_id}&layer=${layer}`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiGetBitbakeComponentVulnerabilities(component_id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake?action=get_vulnerabilities&component_id=${component_id}`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiDeleteBitbakeLicense(id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete_license',
            license_id: id,
        })
    })
    return response
}

export async function apiGetBitbakeComponentComments(component_id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake?action=get_component_comments&component_id=${component_id}`, {
        method: 'GET',
    })
    const comments = await response.json()
    return comments
}

export async function apiAddBitbakeComponentComment(user_id, component_id, comment) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add_component_comment',
            user_id: user_id,
            component_id: component_id,
            comment: comment
        })
    })
    return response
}

export async function apiDeleteBitbakeComponentComment(comment_id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete_component_comment',
            comment_id: comment_id
        })
    })
    return response
}

export async function apiGetBitbakeVulnComments(vuln_id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake?action=get_vuln_comments&vuln_id=${vuln_id}`, {
        method: 'GET',
    })
    const comments = await response.json()
    return comments
}

export async function apiAddBitbakeVulnComment(user_id, vuln_id, comment) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add_vuln_comment',
            user_id: user_id,
            vuln_id: vuln_id,
            comment: comment
        })
    })
    return response
}

export async function apiDeleteBitbakeVulnComment(comment_id) {
    const response = await authFetch(`${process.env.BACKEND_URL}/bitbake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete_vuln_comment',
            comment_id: comment_id
        })
    })
    return response
}