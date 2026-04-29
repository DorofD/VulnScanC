# Vulnerabilities API

## Endpoints

### `GET /vulnerabilities`
Retrieves a list of vulnerabilities for a specific component.

- **Auth**: Required.
- **Query Params**:
  - `component_id` (required): The ID of the component.

**Success Response**
- Code: 200 OK
- **Response Body**: Array of vulnerability objects.
