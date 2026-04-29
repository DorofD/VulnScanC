# Projects API

## Endpoints

### List Projects
`GET /projects`

Returns a list of all projects available in the system.

- **Auth**: Required.

**Success Response**
- Code: 200 OK
- **Response Body**: Array of project objects.

---

### Create / Update / Delete Project
`POST /projects`

Creates, updates, or deletes a project.

- **Auth**: Required.

**Request Body** (JSON):

Create:
```json
{
  "action": "add",
  "name": "New Project Name",
  "description": "Optional description"
}
```

Update:
```json
{
  "action": "change",
  "id": 1,
  "name": "Updated Project Name",
  "description": "Updated description"
}
```

Delete:
```json
{
  "action": "delete",
  "id": 1
}
```

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}`
