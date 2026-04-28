# SARIF API

## Endpoints

### GET /sarif
Works with SARIF files.

- **Auth**: Required.
- **Query Params**:
  - `action=get_filenames` — returns a list of SARIF filenames
  - `action=get_file&filename=...` — downloads a SARIF file as an attachment

---

### POST /sarif
Uploads or deletes SARIF files.

- **Auth**: Required.
- **Actions**:

  **Upload** (multipart/form-data):
  - `file`: The SARIF file to upload
  - `action`: `"upload"`
  - `project_name` (optional): Project name

  **Delete** (JSON):
  ```json
  {
    "action": "delete",
    "filename": "..."
  }
  ```

**Success Response (upload)**
- Code: 200 OK
- Response Body: `{"success": true, "message": "File {filename} uploaded successfully"}`

**Error Response (upload)**
- Code: 400 Bad Request
- Response Body: `{"success": false, "message": "File not uploaded for project {project_name}"}`

**Success Response (delete)**
- Code: 200 OK
- Response Body: `{"success": true}`
