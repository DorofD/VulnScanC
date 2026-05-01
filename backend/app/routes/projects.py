from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from app.services.api_services.projects import get_projects, add_project, delete_project, change_project

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects', methods=['GET', 'POST'])
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
        print(data['action'])
        if data['action'] == 'add':
            try:
                add_project(data['name'], data['description'])
            except KeyError:
                add_project(data['name'], '')
        if data['action'] == 'delete':
            delete_project(data['id'])
        if data['action'] == 'change':
            try:
                new_name = data['name']
            except KeyError:
                new_name = ''
            try:
                new_description = data['description']
            except KeyError:
                new_description = ''
            print(new_description)
            change_project(
                data['id'],
                new_name,
                new_description
            )
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
