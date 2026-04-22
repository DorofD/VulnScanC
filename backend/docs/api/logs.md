# Logs API

## Endpoints

### `GET /logs`
Retrieves logs.

- **Auth**: Required.
- **Query Params**:
  - `action=get_json`: Returns logs in JSON format.
  - `action=get_file`: Returns the log file as an attachment.

### `POST /logs`
Manages log files.

- **Auth**: Required.
- **Actions**:
  - `clear`: `{"action": "clear"}`. Deletes log files.
- **Success Response**: `200 OK` with `{"success": true}`.
