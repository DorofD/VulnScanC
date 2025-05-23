from app.services.bitbake.bitbake_handler import BitbakeHandler


def handle_bb_cve_report(project_name, cve_report):
    bb = BitbakeHandler()
    report_data = bb.parse_cve_report(cve_report)
    bb.save_report_results(project_name, report_data)
    return True


def handle_bb_licenses(license_file):
    bb = BitbakeHandler()
    licenses_data = bb.parse_licenses(license_file)
    bb.update_licenses(licenses_data)
    return True


def add_bitbake_project(project_name):
    bb = BitbakeHandler()
    return bb.add_project(project_name)


def add_bitbake_license(component_id, license_name, recipe_name):
    bb = BitbakeHandler()
    return bb.add_license(component_id, license_name, recipe_name)


def delete_bitbake_project(project_id):
    bb = BitbakeHandler()
    return bb.delete_project(project_id)


def delete_bitbake_license(license_id):
    bb = BitbakeHandler()
    return bb.delete_license(license_id)


def change_bitbake_project(project_id, new_project_name):
    bb = BitbakeHandler()
    return bb.change_project(project_id, new_project_name)


def get_bitbake_projects():
    bb = BitbakeHandler()
    return bb.get_projects()


def get_bitbake_components(project_id, layer):
    bb = BitbakeHandler()
    return bb.get_components(project_id, layer)


def get_bitbake_vulnerabilities(component_id):
    bb = BitbakeHandler()
    return bb.get_vulnerabilities(component_id)
