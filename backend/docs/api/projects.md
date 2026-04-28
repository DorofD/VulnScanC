# Projects API Reference

This document describes the API endpoints for managing projects.

## Endpoints

### List Projects
`GET /projects`

Returns a list of all projects available in the system.

**Response Body**
```json
[
  {
    "id": 1,
    "name": "Example Project",
    "description": "A description of the project"
  },
  ...
]
```

**Success Response**
- Code: 200 OK

---

### Create / Update / Delete Project
`POST /projects`

Creates, updates, or deletes a project.

**Request Body**

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
- Response Body: `{"success": true}`
