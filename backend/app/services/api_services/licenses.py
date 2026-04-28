from app.services.licenses.license_checker import LicenseChecker
from app.pg_repository.queries.licenses import DBLicenses

def check_licenses(project_id):
    checker = LicenseChecker()
    checker.check_project_licenses(project_id)
    return True


def add_license(component_id, key, name, spdx_id, url):
    db_licenses = DBLicenses()
    db_licenses.add_license(component_id, key, name, spdx_id, url)
    return True


def delete_license(id):
    db_licenses = DBLicenses()
    db_licenses.delete_license(id)
    return True
