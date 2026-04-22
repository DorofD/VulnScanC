# Authentication API

## Endpoints

### `POST /login`
Authenticates a user.

- **Request Body**: `{"login": "...", "password": "..."}`
- **Success Response**: `200 OK`
  - **Body**: `{"success": true, "body": {...}, "access_token": "..."}`
  - **Cookies**: Sets `refresh_token` in a cookie.
- **Error Response**: `401 Unauthorized`
  - **Body**: `{"success": false}`

### `POST /refresh`
Refreshes the access token using a valid refresh token.

- **Success Response**: `200 OK`
  - **Body**: `{"success": true, "access_token": "..."}`
  - **Cookies**: Sets a new `refresh_token` in a cookie.
