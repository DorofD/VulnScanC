from app.services.licenses.license_checker import LicenseChecker
from app.repository.queries.licenses import delete_license as delete_license_db
from app.repository.queries.licenses import add_license as add_license_db


def check_licenses(project_id):
    checker = LicenseChecker()
    checker.check_project_licenses(project_id)
    return True


def add_license(component_id, key, name, spdx_id, url):
    add_license_db(component_id, key, name, spdx_id, url)
    return True


def delete_license(id):
    delete_license_db(id)
    return True
