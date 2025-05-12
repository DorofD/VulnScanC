from app.services.bitbake.bitbake_handler import BitbakeHandler


def handle_bb_cve_report(project_name, cve_report):
    bb = BitbakeHandler()
    report_data = bb.parse_cve_report(cve_report)
    bb.save_report_results(project_name, report_data)


def add_bitbake_project(project_name):
    bb = BitbakeHandler()
    return bb.add_project(project_name)


def delete_bitbake_project(project_id):
    bb = BitbakeHandler()
    return bb.delete_project(project_id)


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
