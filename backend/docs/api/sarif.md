# SARIF API

## Endpoints

### `GET /sarif`
Works with SARIF files.

- **Auth**: Required.

**Query Params**:

- `action=get_filenames`:
  - Returns a list of SARIF filenames.

- `action=get_file`:
  - Downloads a SARIF file as an attachment.
  - **Required**: `filename`

---

### `POST /sarif`
Uploads or deletes SARIF files.

- **Auth**: Required.

**Request Formats**:

- **Upload** (`multipart/form-data`):
  - `action`: `"upload"`
  - `file`: The SARIF file to upload
  - `project_name` (optional): Project name

- **Delete** (`application/json`):
  - `action`: `"delete"`
  - `filename`: The filename to delete

**Success Response (upload)**
- Code: 200 OK
- **Response Body**: `{"success": true, "message": "File {filename} uploaded successfully"}`

**Error Response (upload)**
- Code: 400 Bad Request
- **Response Body**: `{"success": false, "message": "File not uploaded for project {project_name}"}`

**Success Response (delete)**
- Code: 200 OK
- **Response Body**: `{"success": true}`
