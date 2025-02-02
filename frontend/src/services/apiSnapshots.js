export async function apiGetProjectSnapshots(project_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/snapshots?project_id=${project_id}`, {
        method: 'GET',
    })
    const snapshots = await response.json()
    return snapshots
}

export async function apiDeleteSnapshot(id) {
    const response = await fetch(`${process.env.BACKEND_URL}/snapshots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            snapshot_id: id,
        })
    })
    return response
}
