# BDU Module

## Overview
The BDU service handles the integration with the FSTEC BDU (БДУ ФСТЭК).

## Implementation Details
- **Data Source**: `https://bdu.fstec.ru/files/documents/vulxml.zip`
- **Archive Structure**: The service expects `export/vulxml.xml` inside the ZIP archive.
- **Update Process**:
  1. `update_bdu`: Downloads the ZIP archive, extracts `export/vulxml.xml` to the local `data/` directory, and cleans up the archive.
  2. `update_vulns`: Parses the local XML and adds new vulnerabilities to the database that are not already present.

For detailed API endpoint descriptions, see the [BDU API](./api/bdu.md).

## Testing
- **Unit tests**: Located in `../tests/test_bdu_fstec.py`.
For more information on the testing strategy, see [Testing Documentation](./tests.md).

