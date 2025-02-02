export async function apiAuth(username, password) {
    const response = await fetch(`${process.env.BACKEND_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            login: username,
            password: password
        })
    })
    return response
}