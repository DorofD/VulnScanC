# Authentication API

## Endpoints

### `POST /login`
Authenticates a user.

- **Request Body** (JSON):
  - `login` (required): User's login identifier.
  - `password` (required): User's password.

**Success Response**
- Code: 200 OK
- **Body**: `{"success": true, "body": {...}, "access_token": "..."}`
- **Cookies**: Sets `refresh_token` in a cookie. The `secure` and `httponly` flags are determined by the `REFRESH_TOKEN_COOKIE_SECURE` environment variable.

**Error Response**
- Code: 401 Unauthorized
- **Body**: `{"success": false}`

---

### `POST /refresh`
Refreshes the access token using a valid refresh token.

- **Auth**: Required (Refresh Token).

**Success Response**
- Code: 200 OK
- **Body**: `{"success": true, "access_token": "..."}`
- **Cookies**: Sets a new `refresh_token` in a cookie. The `secure` and `httponly` flags are determined by the `REFRESH_TOKEN_COOKIE_SECURE` environment variable.
