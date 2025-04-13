export async function apiGetSarifFilesList() {
    const response = await fetch(`${process.env.BACKEND_URL}/sarif?action=get_filenames`, {
        method: 'GET',
    })
    const files = await response.json()
    return files
}

export async function apiGetSarifFile(filename) {
    const response = await fetch(`${process.env.BACKEND_URL}/sarif?action=get_file&filename=${filename}`, {
        method: 'GET',
    })
    if (!response.ok) {
        throw new Error(`Ошибка загрузки файла: ${response.statusText}`);
    }
    const fileBlob = await response.blob();
    return fileBlob;
}

export async function apiDeleteSarifFile(filename) {
    const response = await fetch(`${process.env.BACKEND_URL}/sarif`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'delete',
            filename: filename
        })
    })
    return response
}

