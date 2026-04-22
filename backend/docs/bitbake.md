# Bitbake API

## Endpoints

### `GET /bitbake`
Retrieves Bitbake-related data.

- **Query Params**:
  - `action=get_projects`: Returns list of projects.
  - `action=get_components`: Returns components for a project/layer. Requires `project_id` and `layer`.
  - `action=get_vulnerabilities`: Returns vulnerabilities for a component. Requires `component_id`.
  - `action=get_component_comments`: Returns comments for a component. Requires `component_id`.
  - `action=get_vuln_comments`: Returns comments for a vulnerability. Requires `vuln_id`.

### `POST /bitbake`
Performs Bitbake management actions.

- **Multipart/Form-Data**:
  - `action=upload_cve`: Uploads a CVE report. Requires `file` and `project`.
  - `action=upload_licenses`: Uploads a license manifest. Requires `file`.
- **JSON**:
  - `add_project`: `{"action": "add_project", "project_name": "..."}`
  - `delete_project`: `{"action": "delete_project", "project_id": ...}`
  - `change_project`: `{"action": "change_project", "project_id": ..., "project_name": "..."}`
  - `add_license`: `{"action": "add_license", "component_id": ..., "license_name": "...", "recipe_name": "..."}`
  - `delete_license`: `{"action": "delete_license", "license_id": ...}`
  - `add_component_comment`: `{"action": "add_component_comment", "user_id": ..., "component_id": ..., "comment": "..."}`
  - `delete_component_comment`: `{"action": "delete_component_comment", "comment_id": ...}`
  - `add_vuln_comment`: `{"action": "add_vuln_comment", "user_id": ..., "vuln_id": ..., "comment": "..."}`
  - `delete_vuln_comment`: `{"action": "delete_vuln_comment", "comment_id": ...}`
