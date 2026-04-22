# BDU API

## Endpoints

### `GET /bdu`
Retrieves BDU information.

- **Auth**: Required.
- **Query Params**:
  - `action=get_info`: Returns general BDU information.
  - `action=get_component_vulns`: Returns BDU vulnerabilities for a component. Requires `component_id` and `component_type`.

### `POST /bdu`
Updates BDU data.

- **Auth**: Required.
- **Actions**:
  - `update_bdu`: `{"action": "update_bdu"}`. Downloads and extracts the latest BDU XML archive from FSTEC.
  - `update_vulns`: `{"action": "update_vulns"}`. Synchronizes BDU vulnerabilities with the local database.
- **Success Response**: `200 OK` with `{"success": true}`.

## Implementation Details

### FSTEC BDU Service
The BDU service handles the integration with the FSTEC BDU (БДУ ФСТЭК).

- **Data Source**: `https://bdu.fstec.ru/files/documents/vulxml.zip`
- **Archive Structure**: The service expects `export/vulxml.xml` inside the ZIP archive.
- **Update Process**:
  1. `update_bdu`: Downloads the ZIP archive, extracts `export/vulxml.xml` to the local `data/` directory, and cleans up the archive.
  2. `update_vulns`: Parses the local XML and adds new vulnerabilities to the database that are not already present.
- **Testing**: Unit tests are located in `backend/tests/test_bdu_fstec.py`.
