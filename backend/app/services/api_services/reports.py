from app.services.reports.docx_generator import DOCX_GENERATOR


def create_osv_report(snapshot_id, severities_string):
    dg = DOCX_GENERATOR()
    result = dg.create_osv_report(snapshot_id, severities_string)
    return result


def create_bdu_report(snapshot_id, severities_string):
    dg = DOCX_GENERATOR()
    result = dg.create_bdu_report(snapshot_id, severities_string)
    return result


def create_dependency_track_report(project_uuid):
    dg = DOCX_GENERATOR()
    result = dg.create_dependency_track_report(project_uuid)
    return result


def create_svacer_report(project_name, ids):
    dg = DOCX_GENERATOR()
    result = dg.create_svacer_report(project_name, ids)
    return result
