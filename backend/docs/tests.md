# Testing Documentation

This document provides information on how to run and maintain tests within the backend.

## How to Run Tests

All tests are executed using `unittest` within the project's virtual environment.

### Running All Tests
To run all tests in the project:
```bash
PYTHONPATH=. ./venv/bin/python3 -m unittest discover tests
```

### Running Specific Tests
To run a specific test file:
```bash
PYTHONPATH=. ./venv/bin/python3 -m unittest tests.test_bdu_fstec -v
```

## Test Coverage

### BDU Service (`FSTEC`)
The BDU service is covered by tests in `tests/test_bdu_fstec.py`.

**Covered Scenarios:**
- **`update_bdu`**:
  - Successful download and extraction of `export/vulxml.xml`.
  - Error handling for failed downloads (e.g., 404).
  - Error handling for missing XML files within the ZIP archive.
- **`find_vulns_by_cve_id`**:
  - Successful parsing of XML and matching of CVE identifiers (`test_find_vulns_by_cve_id_success`).
  - Handling of cases where no CVE matches are found (`test_find_vulns_by_cve_id_no_match`).
- **`update_vulns`**:
  - Verification that new vulnerabilities are correctly identified and passed to the repository for insertion.

### Search Data Service (`SearchDataService`)
The Search Data service is covered by tests in `tests/test_search_data.py`.

**Covered Scenarios:**
- **`save_search_data`**:
  - Happy path: project found, new components added, vulnerabilities checked, snapshot created (`test_save_search_data_happy_path`).
  - Project not found: raises `Exception` with "Project not found" message (`test_save_search_data_project_not_found`).
  - No new components: all dependency directories already exist as components, `add_component` is not called (`test_save_search_data_no_new_components`).
  - New vulnerabilities: `add_vulnerabilities` is called with vulnerabilities not already in the database (`test_save_search_data_adds_new_vulnerabilities`).

## Test Structure

- **`tests/`**: Contains all unit and integration tests.
- **`tests/test_data/`**: Contains test data files (e.g., `test_deps.json`, `test_vulns.json`).
- **Mocking**: We heavily use `unittest.mock` to isolate the business logic from external dependencies like `requests`, `os`, `zipfile`, and the database.
