# Components API

## Endpoints

### GET /components
Returns a list of components for a project.

- **Auth**: Required.
- **Query Params**:
  - `project_id` (required): Project ID

---

### POST /components
Changes the status of a component.

- **Auth**: Required.
- **Request Body**:
  - `component_id` (required): Component ID
  - `new_status` (required): New status

**Success Response**
- Code: 200 OK
- Response Body: `{"success": true}`
