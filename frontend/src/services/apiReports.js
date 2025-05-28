export async function apiGetOsvReport(snapshot_id, severities, project_name, snapshot_datetime) {
    try {
        const severitiesString = severities.join('');
        const response = await fetch(`${process.env.BACKEND_URL}/reports?report_type=osv&snapshot_id=${snapshot_id}&severities=${severitiesString}`, {
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
        const contentDisposition = response.headers.get('Content-Disposition');
        console.log(response.headers)
        a.download = `${project_name} ${snapshot_datetime}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        // document.body.removeChild(a); 
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was an error downloading the report:', error);
        throw new Error('There was an error downloading the report:', error);
    }
}

export async function apiGetBduReport(snapshot_id, severities, project_name, snapshot_datetime) {
    try {
        const severitiesString = severities.join('');
        const response = await fetch(`${process.env.BACKEND_URL}/reports?report_type=bdu&snapshot_id=${snapshot_id}&severities=${severitiesString}`, {
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
        const contentDisposition = response.headers.get('Content-Disposition');
        console.log(response.headers)
        a.download = `${project_name} ${snapshot_datetime}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        // document.body.removeChild(a); 
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was an error downloading the report:', error);
        throw new Error('There was an error downloading the report:', error);
    }
}

export async function apiGetBitbakeReport(snapshot_id, severities, layers, project_name, snapshot_datetime) {
    try {
        const severitiesString = severities.join(',');
        const layersString = layers.join(',');
        const response = await fetch(`${process.env.BACKEND_URL}/reports?report_type=bitbake&snapshot_id=${snapshot_id}&severities=${severitiesString}&layers=${layersString}`, {
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
        const contentDisposition = response.headers.get('Content-Disposition');
        console.log(response.headers)
        a.download = `${project_name} ${snapshot_datetime}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        // document.body.removeChild(a); 
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was an error downloading the report:', error);
        throw new Error('There was an error downloading the report:', error);
    }
}

export async function apiGetBitbakeBduReport(snapshot_id, severities, layers, project_name, snapshot_datetime) {
    try {
        const severitiesString = severities.join(',');
        const layersString = layers.join(',');
        const response = await fetch(`${process.env.BACKEND_URL}/reports?report_type=bitbake_bdu&snapshot_id=${snapshot_id}&severities=${severitiesString}&layers=${layersString}`, {
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
        const contentDisposition = response.headers.get('Content-Disposition');
        console.log(response.headers)
        a.download = `${project_name} ${snapshot_datetime}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        // document.body.removeChild(a); 
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was an error downloading the report:', error);
        throw new Error('There was an error downloading the report:', error);
    }
}

export async function apiGetSvacerReport(project_name, project_id, branch_id, snapshot_id, snapshot_name) {
    try {
        const response = await fetch(`${process.env.BACKEND_URL}/reports?report_type=svacer&project_name=${project_name}&project_id=${project_id}&branch_id=${branch_id}&snapshot_id=${snapshot_id}`, {
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
        const contentDisposition = response.headers.get('Content-Disposition');
        console.log(response.headers)
        a.download = snapshot_name;
        document.body.appendChild(a);
        a.click();
        a.remove();
        // document.body.removeChild(a); 
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was an error downloading the report:', error);
        throw new Error('There was an error downloading the report:', error);
    }
}

export async function apiGetDependencyTrackReport(project_uuid, project_name) {
    try {
        const response = await fetch(`${process.env.BACKEND_URL}/reports?report_type=dependency_track&project_uuid=${project_uuid}`, {
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
        const contentDisposition = response.headers.get('Content-Disposition');
        console.log(response.headers)
        a.download = project_name;
        document.body.appendChild(a);
        a.click();
        a.remove();
        // document.body.removeChild(a); 
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('There was an error downloading the report:', error);
        throw new Error('There was an error downloading the report:', error);
    }
}
