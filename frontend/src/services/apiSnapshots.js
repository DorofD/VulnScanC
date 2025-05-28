export async function apiGetProjectSnapshots(project_type, project_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/snapshots?project_id=${project_id}&&project_type=${project_type}`, {
        method: 'GET',
    })
    const snapshots = await response.json()
    return snapshots
}

export async function apiDeleteSnapshot(project_type, id) {
    const response = await fetch(`${process.env.BACKEND_URL}/snapshots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            project_type: project_type,
            snapshot_id: id,
        })
    })
    return response
}
