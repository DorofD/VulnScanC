export async function apiCheckLicenses(project_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/licenses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'check_licenses',
            project_id: project_id,
        })
    })
    return response
}

export async function apiDeleteLicense(license_id) {
    const response = await fetch(`${process.env.BACKEND_URL}/licenses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            license_id: license_id,
        })
    })
    return response
}
