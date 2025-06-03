import { authFetch } from './authFetch';

export async function apiGetBinaryInfo() {
    const response = await authFetch(`${process.env.BACKEND_URL}/binary?action=get_info`, {
        method: 'GET',
    })
    return response
}

export async function apiGetBinaryFile() {
    try {
        const response = await authFetch(`${process.env.BACKEND_URL}/binary?action=get_file`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = "executable_module";
        document.body.appendChild(a);
        a.click();
        a.remove();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was an error downloading the report:', error);
    }
}

export async function apiBuildBinary() {
    const response = await authFetch(`${process.env.BACKEND_URL}/binary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'build_binary'
        })
    })
    return response
}