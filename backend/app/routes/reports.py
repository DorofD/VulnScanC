from flask import Blueprint, request, current_app, send_file, jsonify
from flask_jwt_extended import jwt_required

from app.services.api_services.reports import create_osv_report, create_bdu_report, create_dependency_track_report
from app.services.api_services.reports import create_svacer_report, create_bitbake_report, create_bitbake_bdu_report

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports', methods=(['GET']))
def reports():
    report_type = request.args.get('report_type')

    if report_type == 'osv':
        if not request.args.get('snapshot_id'):
            return jsonify({
                'error': 'Missing required parameters: snapshot_id',
            }), 400
        snapshot_id = request.args.get('snapshot_id')
        severities_string = request.args.get('severities')
        report = create_osv_report(snapshot_id, severities_string)
        report_name = f"osv_report_{report['project_name']}_{report['datetime']}.docx"
        response = send_file(
            path_or_file=report['report'],
            as_attachment=True,
            download_name=report_name,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{report_name}"'
        current_app.logger.info(f'Sent OSV report: {report_name}')
        return response

    elif report_type == 'bdu':
        snapshot_id = request.args.get('snapshot_id')
        severities_string = request.args.get('severities')
        report = create_bdu_report(snapshot_id, severities_string)
        report_name = f"bdu_report_{report['project_name']}_{report['datetime']}.docx"
        response = send_file(
            path_or_file=report['report'],
            as_attachment=True,
            download_name=report_name,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{report_name}"'
        current_app.logger.info(f'Sent BDU report: {report_name}')
        return response

    elif report_type == 'svacer':
        required_params = ['project_id', 'branch_id',
                           'snapshot_id', 'project_name']
        missing_params = [
            param for param in required_params if not request.args.get(param)]
        if missing_params:
            return jsonify({
                'error': f"Missing required parameters: {missing_params}",
            }), 400
        project_name = request.args.get('project_name')
        project_id = request.args.get('project_id')
        branch_id = request.args.get('branch_id')
        snapshot_id = request.args.get('snapshot_id')
        report = create_svacer_report(
            project_name, ids=[project_id, branch_id, snapshot_id])
        current_app.logger.info(f"Sent Svacer report: {project_name}")
        return send_file(path_or_file=report['report'], as_attachment=True, download_name=report['report_name'], mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    elif report_type == 'dependency_track':
        required_params = ['project_uuid']
        missing_params = [
            param for param in required_params if not request.args.get(param)]
        if missing_params:
            return jsonify({
                'error': f"Missing required parameters: {missing_params}",
            }), 400

        project_uuid = request.args.get('project_uuid')
        report = create_dependency_track_report(project_uuid)
        current_app.logger.info(
            f"Sent Dependency-Track report for project with uuid: {project_uuid}")
        return send_file(path_or_file=report['report'], as_attachment=True, download_name=report['report_name'], mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    elif report_type == 'bitbake':
        snapshot_id = request.args.get('snapshot_id')
        severities_string = request.args.get('severities')
        layers_string = request.args.get('layers')
        # print(report_type)
        # print(severities_string)
        # print(layers_string)
        report = create_bitbake_report(
            snapshot_id, layers_string, severities_string)
        report_name = f"bitbake_report_{report['project_name']}_{report['datetime']}.docx"
        response = send_file(
            path_or_file=report['report'],
            as_attachment=True,
            download_name=report_name,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{report_name}"'
        current_app.logger.info(f'Sent BDU report: {report_name}')
        return response

    elif report_type == 'bitbake_bdu':
        snapshot_id = request.args.get('snapshot_id')
        severities_string = request.args.get('severities')
        layers_string = request.args.get('layers')
        print(report_type)
        print(severities_string)
        print(layers_string)
        # report = create_bdu_report(snapshot_id, severities_string)
        # report_name = f"bdu_report_{report['project_name']}_{report['datetime']}.docx"
        # response = send_file(
        #     path_or_file=report['report'],
        #     as_attachment=True,
        #     download_name=report_name,
        #     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        # )
        # response.headers['Content-Disposition'] = f'attachment; filename="{report_name}"'
        # current_app.logger.info(f'Sent BDU report: {report_name}')
        # return response
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return jsonify({
            'error': f"Invalid type: {report_type}. Valid values: osv, svacer, dependency_track",
        }), 400
