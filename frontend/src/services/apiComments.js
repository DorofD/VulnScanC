export async function apiGetComponentComments(component_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/comments?type=component&component_id=${component_id}`, {
        method: 'GET',
    })
    const comments = await response.json()
    return comments
}

export async function apiAddComponentComment(user_id, component_id, comment) {
    const response = await fetch(`${process.env.BACKEND_URL}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'add',
            type: 'component',
            user_id: user_id,
            component_id: component_id,
            comment: comment
        })
    })
    return response
}

export async function apiDeleteComponentComment(comment_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            type: 'component',
            comment_id: comment_id
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