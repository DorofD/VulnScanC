# Bitbake API

## Endpoints

### `GET /bitbake`
Retrieves Bitbake-related data.

- **Auth**: Not explicitly marked in docs, but follows general pattern.

**Query Params**:

- `action=get_projects`:
  - Returns list of projects (includes `project_id`, `project_name`, and layers).

- `action=get_components`:
  - Returns components for a project/layer.
  - **Required**: `project_id`, `layer`

- `action=get_vulnerabilities`:
  - Returns vulnerabilities for a component.
  - **Required**: `component_id`

- `action=get_component_comments`:
  - Returns comments for a component.
  - **Required**: `component_id`

- `action=get_vuln_comments`:
  - Returns comments for a vulnerability.
  - **Required**: `vuln_id`

**Success Response**
- Code: 200 OK
- **Response Body**: Array of project, component, vulnerability, or comment objects.

---

### `POST /bitbake`
Performs Bitbake management actions.

- **Auth**: Not explicitly marked in docs, but follows general pattern.

**Request Formats**:

- **Multipart/Form-Data**:

  - `action=upload_cve`:
    - Uploads a CVE report.
    - **Required**: `file`, `project` (project name)

  - `action=upload_licenses`:
    - Uploads a license manifest.
    - **Required**: `file`

- **JSON**:

  - `action=add_project`:
    - **Required**: `project_name`

  - `action=delete_project`:
    - **Required**: `project_id`

  - `action=change_project`:
    - **Required**: `project_id`, `project_name`

  - `action=add_license`:
    - **Required**: `component_id`, `license_name`, `recipe_name`

  - `action=delete_license`:
    - **Required**: `license_id`

  - `action=add_component_comment`:
    - **Required**: `user_id`, `component_id`, `comment`

  - `action=delete_component_comment`:
    - **Required**: `comment_id`

  - `action=add_vuln_comment`:
    - **Required**: `user_id`, `vuln_id`, `comment`

  - `action=delete_vuln_comment`:
    - **Required**: `comment_id`

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}` or plain text status.

**Error Response**
- Code: 400 Bad Request — `"Invalid request"`
