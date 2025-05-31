from flask import Blueprint, request

from app.services.api_services.bitbake import add_bitbake_project, delete_bitbake_project, change_bitbake_project, get_bitbake_projects
from app.services.api_services.bitbake import get_bitbake_components, get_bitbake_vulnerabilities, handle_bb_cve_report, handle_bb_licenses, delete_bitbake_license, add_bitbake_license
from app.services.api_services.bitbake import add_bitbake_component_comment, delete_bitbake_component_comment, get_bitbake_comments_for_component
from app.services.api_services.bitbake import add_bitbake_vulnerability_comment, delete_bitbake_vulnerability_comment, get_bitbake_comments_for_vulnerability


bitbake_bp = Blueprint('bitbake', __name__)


@bitbake_bp.route('/bitbake', methods=['GET', 'POST'])
def bitbake():
    if request.method == 'GET':
        if request.args.get('action') == 'get_projects':
            # возвращает project_id, project_name, и слои проекта
            return get_bitbake_projects()
        if request.args.get('action') == 'get_components':
            # возвращает компоненты по id проекта и слою
            project_id = request.args.get('project_id')
            layer = request.args.get('layer')
            return get_bitbake_components(project_id, layer)
        if request.args.get('action') == 'get_vulnerabilities':
            component_id = request.args.get('component_id')
            return get_bitbake_vulnerabilities(component_id)
        if request.args.get('action') == 'get_component_comments':
            component_id = request.args.get('component_id')
            return get_bitbake_comments_for_component(component_id)
        if request.args.get('action') == 'get_vuln_comments':
            vuln_id = request.args.get('vuln_id')
            return get_bitbake_comments_for_vulnerability(vuln_id)
    if request.method == 'POST':
        # отправить отчёт cve
        # curl -X POST -F "file=@./report.cve" -F "action=upload_cve"-F "project=project_name" http://192.168.1.2:5000/bitbake
        if 'file' in request.files and request.form['action'] == 'upload_cve':
            project = request.form['project']
            file = request.files['file']
            handle_bb_cve_report(project, file)
            return "File processed successfully!", 200
        # отправить лицензии
        # curl -X POST -F "file=@./license.manifest" -F "action=upload_licenses" http://192.168.1.2:5000/bitbake
        if 'file' in request.files and request.form['action'] == 'upload_licenses':
            file = request.files['file']
            handle_bb_licenses(file)
            return "File processed successfully!", 200
        data = request.json
        if data['action'] == 'add_project':
            if add_bitbake_project(data['project_name']):
                return "Project created", 200
        if data['action'] == 'delete_project':
            if delete_bitbake_project(data['project_id']):
                return "Project deleted", 200
        if data['action'] == 'change_project':
            if change_bitbake_project(data['project_id'], data['project_name']):
                return "Project changed", 200
        if data['action'] == 'add_license':
            if add_bitbake_license(data['component_id'], data['license_name'], data['recipe_name']):
                return "License added", 200
        if data['action'] == 'delete_license':
            if delete_bitbake_license(data['license_id']):
                return "License deleted", 200
        if data['action'] == 'add_component_comment':
            if add_bitbake_component_comment(data['user_id'], data['component_id'], data['comment']):
                return "Comment added", 200
        if data['action'] == 'delete_component_comment':
            if delete_bitbake_component_comment(data['comment_id']):
                return "Comment deleted", 200
        if data['action'] == 'add_vuln_comment':
            if add_bitbake_vulnerability_comment(data['user_id'], data['vuln_id'], data['comment']):
                return "Comment added", 200
        if data['action'] == 'delete_vuln_comment':
            if delete_bitbake_vulnerability_comment(data['comment_id']):
                return "Comment deleted", 200
    return "Invalid request", 400
