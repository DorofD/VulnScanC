export async function apiGetLogsJson() {
    const response = await fetch(`${process.env.BACKEND_URL}/logs?action=get_json`, {
        method: 'GET',
    })
    const projects = await response.json()
    return projects
}

export async function apiGetLogsFile() { 
    try {
        const response = await fetch(`${process.env.BACKEND_URL}/logs?action=get_file`, { 
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
        a.download = `app.log`; 
        document.body.appendChild(a); 
        a.click();
        a.remove(); 
        document.body.removeChild(a); 
        window.URL.revokeObjectURL(url); 
    } catch (error) {
        console.error('There was an error downloading log file:', error);
    }
}