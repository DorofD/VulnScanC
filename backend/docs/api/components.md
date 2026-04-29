# Components API

## Endpoints

### `GET /components`
Retrieves a list of components for a specific project.

- **Auth**: Required.
- **Query Params**:
  - `project_id` (required): The ID of the project.

### `POST /components`
Changes the status of a component.

- **Auth**: Required.
- **Request Body** (JSON):
  - `component_id` (required): The ID of the component.
  - `new_status` (required): The new status to apply.

**Success Response**
- Code: 200 OK
- Response Body: `{"success": true}`
