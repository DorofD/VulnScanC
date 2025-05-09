from flask import Blueprint, current_app, request, jsonify, send_file, abort
from flask_cors import cross_origin
import traceback
from app.services.search_data.search_data import save_search_data

from app.services.api_services.projects import get_projects, add_project, delete_project, add_project, change_project
from app.services.api_services.components import get_project_components, change_component_status
from app.services.api_services.vulnerabilities import get_vulnerabilities_by_component
from app.services.api_services.snapshots import get_project_snapshots, delete_snapshot
from app.services.api_services.users import signin, get_users, add_user, delete_user, change_user
from app.services.api_services.svacer import get_projects as get_svacer_projects, get_snapshots as get_svacer_snapshots
from app.services.api_services.dependency_track import get_projects as get_dt_projects, get_components as get_dt_components
from app.services.api_services.logs import get_logs
from app.services.api_services.binary import get_binary_info, build_executable_module
from app.services.api_services.licenses import check_licenses, add_license, delete_license
from app.services.api_services.bdu import get_bdu_info, update_bdu, update_vulns_by_cve_id, get_component_dbu_vulns
from app.services.api_services.reports import create_osv_report, create_bdu_report, create_dependency_track_report, create_svacer_report
from app.services.api_services.component_comments import get_comments_for_component, add_comment_for_component, delete_component_comment
from app.services.api_services.sarif import upload_sarif, get_sarif_path, get_sarif_filenames, delete_sarif
from app.services.api_services.bitbake import handle_bb_cve_report

main = Blueprint('main', __name__)


@main.route('/binary', methods=(['GET', 'POST']))
@cross_origin()
def binary():
    if request.method == 'GET':
        if request.args.get('action') == 'get_info':
            return jsonify(get_binary_info())
        if request.args.get('action') == 'get_file':
            try:
                file_path = '/binary/executable_module'
                return send_file(file_path, as_attachment=True)
            except FileNotFoundError as exc:
                current_app.logger.exception(
                    f'Executable module not found: {exc}')
                abort(404, description="Executable module not found")

    if request.method == 'POST':
        data = request.json
        if data['action'] == 'build_binary':
            build_executable_module()
            current_app.logger.info(f"Executable module has been built")
            return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/search_data', methods=(['POST']))
@cross_origin()
def search_data():
    try:
        data = request.get_json()
        if data['status'] == 'ok':
            save_search_data(data)
            current_app.logger.info(
                f"Data received from Executable Module, the processing was successful! Project: {data['project_name']} Time: {data['datetime']} Pipline ID: {data['pipeline_id']}")
        elif data['status'] == 'fail':
            current_app.logger.error(
                f"Executable Module could not collect the data for project: {data['project_name']}. More details in pipeline: {data['pipeline_id']}")
        response = {
            "message": "Data processed successfully"
        }
        return jsonify(response), 200

    except FileNotFoundError as exc:
        current_app.logger.exception(
            f"Error when handling search data from Executable Module: {exc}")
        abort(404, description="Error when handling search data")


@main.route('/reports', methods=(['GET']))
@cross_origin()
def reports():
    if not request.args.get('type'):
        return jsonify({
            'error': 'Missing required parameters: type',
        }), 400
    else:
        report_type = request.args.get('type')

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

    else:
        return jsonify({
            'error': f"Invalid type: {report_type}. Valid values: osv, svacer, dependency_track",
        }), 400


@main.route('/projects', methods=(['GET', 'POST']))
@cross_origin()
def projects():
    if request.method == 'GET':
        result = get_projects()
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        if data['action'] == 'add':
            add_project(data['name'])
        if data['action'] == 'delete':
            delete_project(data['project_id'])
        if data['action'] == 'change':
            change_project(data['project_id'], data['project_name'])
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/components', methods=(['GET', 'POST']))
@cross_origin()
def components():
    if request.method == 'GET':
        project_id = request.args.get('project_id')
        result = get_project_components(project_id)
        return jsonify(result)
    if request.method == 'POST':
        data = request.json
        change_component_status(data['component_id'], data['new_status'])
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/comments', methods=(['GET', 'POST']))
@cross_origin()
def comments():
    if request.method == 'GET':
        if request.args.get('type') == 'component':
            result = get_comments_for_component(
                request.args.get('component_id'))
            return jsonify(list(reversed(result)))
        if request.args.get('type') == 'vuln':
            pass

    if request.method == 'POST':
        data = request.json
        if data['action'] == 'add':
            if data['type'] == 'component':
                add_comment_for_component(
                    data['user_id'], data['component_id'], data['comment'])
                if data['type'] == 'vuln':
                    pass
        if data['action'] == 'delete':
            if data['type'] == 'component':
                delete_component_comment(data['comment_id'])
            if data['type'] == 'vuln':
                pass
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/licenses', methods=(['POST']))
@cross_origin()
def licenses():
    data = request.json
    if data['action'] == 'check_licenses':
        check_licenses(data['project_id'])
    if data['action'] == 'add':
        add_license(data['component_id'], data['key'],
                    data['name'], data['spdx_id'], data['url'])
    if data['action'] == 'delete':
        delete_license(data['license_id'])
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/vulnerabilities', methods=(['GET']))
@cross_origin()
def vulnerabilities():
    id = request.args.get('component_id')
    result = get_vulnerabilities_by_component(id)
    return jsonify(result)


@main.route('/bdu', methods=(['GET', 'POST']))
@cross_origin()
def bdu():
    if request.method == 'GET':
        if request.args.get('action') == 'get_info':
            result = get_bdu_info()
        elif request.args.get('action') == 'get_component_vulns':
            component_id = request.args.get('component_id')
            result = get_component_dbu_vulns(component_id)
        else:
            return jsonify({'error': f"Missing required parameters", }), 400
        return jsonify(result)
    if request.method == 'POST':
        data = request.json
        if data['action'] == 'update_bdu':
            update_bdu()
        if data['action'] == 'update_vulns':
            update_vulns_by_cve_id()
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/snapshots', methods=(['GET', 'POST']))
@cross_origin()
def snapshots():
    if request.method == 'GET':
        project_id = request.args.get('project_id')
        result = get_project_snapshots(project_id)
        return jsonify(result)
    if request.method == 'POST':
        data = request.json
        if data['action'] == 'delete':
            delete_snapshot(data['snapshot_id'])
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/svacer', methods=(['GET']))
@cross_origin()
def svacer():
    if request.args.get('action') == 'get_projects':
        result = get_svacer_projects()
        return jsonify(result)

    if request.args.get('action') == 'get_snapshots':
        result = get_svacer_snapshots(request.args.get(
            'project_id'), request.args.get('branch_id'))
        return jsonify(result)


@main.route('/dependency_track', methods=(['GET']))
@cross_origin()
def dependency_track():
    if request.args.get('action') == 'get_projects':
        result = get_dt_projects()
        return jsonify(result)

    if request.args.get('action') == 'get_components':
        result = get_dt_components(request.args.get('project_uuid'))
        return jsonify(result)


@main.route('/sarif', methods=(['GET', 'POST']))
@cross_origin()
def sarif():
    if request.method == 'GET':
        if request.args.get('action') == 'get_filenames':
            return get_sarif_filenames()
        if request.args.get('action') == 'get_file':
            return send_file(get_sarif_path(request.args.get('filename')), as_attachment=True)
    if request.method == 'POST':
        if 'file' in request.files and 'action' in request.form:
            file = request.files['file']
            action = request.form['action']
            project_name = request.form.get('project_name')
            if action == 'upload':
                filename = upload_sarif(file, project_name)
                if type(filename) == str:
                    return jsonify({'success': True, 'message': f"File {filename} uploaded successfully"}), 200
                return jsonify({'success': False, 'message': f"File not uploaded for project {project_name}"}), 400
        data = request.json
        if data['action'] == 'delete':
            delete_sarif(data['filename'])
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/bitbake', methods=['GET', 'POST'])
# отправить отчёт
# curl -X POST -F "file=@./report.cve" -F "project=project_name" http://192.168.1.2:5000/bitbake
@cross_origin()
def bitbake():
    if request.method == 'POST':
        if 'file' in request.files and 'project' in request.form:
            project = request.form['project']
            file = request.files['file']
            handle_bb_cve_report(project, file)

            return "File processed successfully!", 200
    return "Invalid request", 400
    #     action = request.form['action']
    #     project_name = request.form.get('project_name')
    #     if action == 'upload':
    #         filename = upload_sarif(file, project_name)
    #         if type(filename) == str:
    #             return jsonify({'success': True, 'message': f"File {filename} uploaded successfully"}), 200
    #         return jsonify({'success': False, 'message': f"File not uploaded for project {project_name}"}), 400
    # data = request.json
    # if data['action'] == 'delete':
    #     delete_sarif(data['filename'])
    # return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/login', methods=(['POST']))
@cross_origin()
def login():
    user = request.json
    auth_result = signin(user['login'], user['password'])
    if auth_result:
        current_app.logger.info(f"User is logged in: {user['login']}")
        return jsonify({'success': True, 'body': auth_result}), 200, {'ContentType': 'application/json'}
    current_app.logger.error(f"User failed to log in: {user['login']}")
    return jsonify({'success': False}), 401, {'ContentType': 'application/json'}


@main.route('/users', methods=(['GET', 'POST']))
@cross_origin()
def users():
    if request.method == 'GET':
        result = jsonify(get_users())
        return result

    if request.method == 'POST':
        data = request.json
        if data['action'] == 'add':
            add_user(data['login'], data['auth_type'],
                     data['role'], data['password'])
        if data['action'] == 'change':
            change_user(data['id'], data['login'], data['role'],
                        data['auth_type'], data['password'])
        if data['action'] == 'delete':
            delete_user(id=data['id'])

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/logs', methods=(['GET', 'POST']))
@cross_origin()
def logs():
    if request.method == 'GET':
        if request.args.get('action') == 'get_json':
            result = get_logs()
            return jsonify(result)

        if request.args.get('action') == 'get_file':
            try:
                import os
                file_path = os.path.join(os.getcwd(), 'data', 'app.log')
                return send_file(file_path, as_attachment=True)
            except FileNotFoundError:
                abort(404, description="Log file not found")


@main.errorhandler(Exception)
def handle_value_error(error):
    print(f"ERROR: {error}")
    traceback.print_exc()
    current_app.logger.exception(f'Backend has unknown error: {error}')
    return jsonify({'error': f'Backend error: {error}'}), 500
