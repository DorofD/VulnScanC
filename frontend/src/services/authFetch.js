export async function authFetch(url, options = {}) {
    const token = localStorage.getItem('accessToken');
    const headers = {
        ...options.headers,
        'Authorization': token,
    };

    let response = await fetch(url, {
        ...options,
        headers,
        credentials: 'include'
    });

    if (response.status === 401 || response.status === 422) {
        try {
            const refreshResponse = await fetch(`${process.env.BACKEND_URL}/refresh`, {
                method: 'POST',
                credentials: 'include'
            });

            if (refreshResponse.ok) {
                const refreshData = await refreshResponse.json();
                const newAccessToken = refreshData.access_token;

                localStorage.setItem('accessToken', newAccessToken);

                headers['Authorization'] = newAccessToken;
                response = await fetch(url, {
                    ...options,
                    headers,
                    credentials: 'include'
                });

                return response;
            } else {
                console.log('Refresh token invalid')
                throw new Error('Refresh token invalid');
            }
        } catch (error) {
            console.error('Ошибка при обновлении токена:', error);
            localStorage.removeItem('accessToken');
            window.location.href = '/login';
        }
    }
    if (response.status === 403) {
        console.log('Forbidden, check your role')
        throw new Error('Forbidden, check your role');
    }

    if (response.status === 500) {
        console.log('500 Internal Server Error')
        throw new Error('500 Internal Server Error');
    }
    return response;
}
