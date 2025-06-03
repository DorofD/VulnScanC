from flask import Blueprint, current_app, request, jsonify, send_file, abort
from flask_jwt_extended import jwt_required, get_jwt
from app.services.search_data.search_data import save_search_data

from app.services.api_services.projects import get_projects, add_project, delete_project, add_project, change_project
from app.services.api_services.components import get_project_components, change_component_status
from app.services.api_services.vulnerabilities import get_vulnerabilities_by_component
from app.services.api_services.binary import get_binary_info, build_executable_module
from app.services.api_services.component_comments import get_comments_for_component, add_comment_for_component, delete_component_comment

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
@jwt_required()
def projects():

    jwt_data = get_jwt()
    user_role = jwt_data.get('role')
    print('User role is:', user_role)
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
@jwt_required()
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
@jwt_required()
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


@main.route('/vulnerabilities', methods=(['GET']))
@jwt_required()
def vulnerabilities():
    id = request.args.get('component_id')
    result = get_vulnerabilities_by_component(id)
    return jsonify(result)
