# Testing Documentation

This document provides information on how to run and maintain tests within the backend.

## How to Run Tests

All tests are executed using `unittest` within the project's virtual environment.

### Running All Tests
To run all tests in the project:
```bash
cd backend && PYTHONPATH=. ./venv/bin/python3 -m unittest discover tests
```

### Running Specific Tests
To run a specific test file:
```bash
cd backend && PYTHONPATH=. ./venv/bin/python3 tests/test_bdu_fstec.py
```

## Test Coverage

### BDU Service (`FSTEC`)
The BDU service is covered by tests in `backend/tests/test_bdu_fstec.py`.

**Covered Scenarios:**
- **`update_bdu`**:
  - Successful download and extraction of `export/vulxml.xml`.
  - Error handling for failed downloads (e.g., 404).
  - Error handling for missing XML files within the ZIP archive.
- **`find_vulns_by_cve_id`**:
  - Successful parsing of XML and matching of CVE identifiers.
  - Handling of cases where no CVE matches are found.
- **`update_vulns`**:
  - Verification that new vulnerabilities are correctly identified and passed to the repository for insertion.

## Test Structure

- **`backend/tests/`**: Contains all unit and integration tests.
- **Mocking**: We heavily use `unittest.mock` to isolate the business logic from external dependencies like `requests`, `os`, `zipfile`, and the database.
