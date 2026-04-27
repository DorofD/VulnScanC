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

### Create Project
`POST /projects`

Creates a new project.

**Request Body**
```json
{
  "name": "New Project Name",
  "description": "Optional description"
}
```

**Success Response**
- Code: 201 Created

---

### Update Project
`PUT /projects`

Updates an existing project's details.

**Query Parameters**
- `id` (required): The ID of the project to update.

**Request Body**
```json
{
  "name": "Updated Project Name",
  "description": "Updated description"
}
```

**Success Response**
- Code: 200 OK

---

### Delete Project
`DELETE /projects`

Deletes a project and its associated data.

**Query Parameters**
- `id` (required): The ID of the project to delete.

**Success Response**
- Code: 200 OK
