# Search Data API

## Endpoints

### POST /search_data
Receives data from the executable module.

- **Auth**: Not required.
- **Request Body**:

  **Success**:
  ```json
  {
    "status": "ok",
    "project_name": "...",
    "datetime": "...",
    "pipeline_id": "..."
  }
  ```

  **Failure**:
  ```json
  {
    "status": "fail",
    "project_name": "...",
    "pipeline_id": "..."
  }
  ```

**Success Response**
- Code: 200 OK
- Response Body: `{"message": "Data processed successfully"}`
