from flask import Blueprint, current_app, request, jsonify, send_file, abort
from flask_jwt_extended import jwt_required
from app.services.search_data.search_data import save_search_data

from app.services.api_services.projects import get_projects, add_project, delete_project, add_project, change_project
from app.services.api_services.components import get_project_components, change_component_status
from app.services.api_services.vulnerabilities import get_vulnerabilities_by_component
from app.services.api_services.snapshots import get_project_snapshots, delete_snapshot, get_bitbake_project_snapshots, delete_bitbake_snapshot
from app.services.api_services.svacer import get_projects as get_svacer_projects, get_snapshots as get_svacer_snapshots
from app.services.api_services.dependency_track import get_projects as get_dt_projects, get_components as get_dt_components
from app.services.api_services.binary import get_binary_info, build_executable_module
from app.services.api_services.licenses import check_licenses, add_license, delete_license
from app.services.api_services.bdu import get_bdu_info, update_bdu, update_vulns_by_cve_id, get_component_bdu_vulns
from app.services.api_services.component_comments import get_comments_for_component, add_comment_for_component, delete_component_comment
from app.services.api_services.sarif import upload_sarif, get_sarif_path, get_sarif_filenames, delete_sarif

main = Blueprint('main', __name__)


@main.route('/binary', methods=(['GET', 'POST']))
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


@main.route('/projects', methods=(['GET', 'POST']))
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
def vulnerabilities():
    id = request.args.get('component_id')
    result = get_vulnerabilities_by_component(id)
    return jsonify(result)


@main.route('/bdu', methods=(['GET', 'POST']))
def bdu():
    if request.method == 'GET':
        if request.args.get('action') == 'get_info':
            result = get_bdu_info()
        elif request.args.get('action') == 'get_component_vulns':
            component_id = request.args.get('component_id')
            component_type = request.args.get('component_type')
            result = get_component_bdu_vulns(component_id, component_type)
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
def snapshots():
    if request.method == 'GET':
        project_type = request.args.get('project_type')
        if project_type == 'common':
            project_id = request.args.get('project_id')
            result = get_project_snapshots(project_id)
            return jsonify(result)
        elif project_type == 'bitbake':
            project_id = request.args.get('project_id')
            result = get_bitbake_project_snapshots(project_id)
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': 'Unkown project type'}), 400, {'ContentType': 'application/json'}
    if request.method == 'POST':
        data = request.json
        project_type = data['project_type']
        if project_type == 'common':
            if data['action'] == 'delete':
                delete_snapshot(data['snapshot_id'])
            return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
        elif project_type == 'bitbake':
            if data['action'] == 'delete':
                delete_bitbake_snapshot(data['snapshot_id'])
            return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
        else:
            return jsonify({'success': False, 'error': 'Unkown project type'}), 400, {'ContentType': 'application/json'}


@main.route('/svacer', methods=(['GET']))
def svacer():
    if request.args.get('action') == 'get_projects':
        result = get_svacer_projects()
        return jsonify(result)

    if request.args.get('action') == 'get_snapshots':
        result = get_svacer_snapshots(request.args.get(
            'project_id'), request.args.get('branch_id'))
        return jsonify(result)


@main.route('/dependency_track', methods=(['GET']))
def dependency_track():
    if request.args.get('action') == 'get_projects':
        result = get_dt_projects()
        return jsonify(result)

    if request.args.get('action') == 'get_components':
        result = get_dt_components(request.args.get('project_uuid'))
        return jsonify(result)


@main.route('/sarif', methods=(['GET', 'POST']))
@jwt_required()
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
