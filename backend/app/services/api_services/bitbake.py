from app.services.bitbake.bitbake_handler import BitbakeHandler


def handle_bb_cve_report(project_name, cve_report):
    bb = BitbakeHandler()
    report_data = bb.parse_cve_report(cve_report)
    bb.save_report_results(project_name, report_data)
