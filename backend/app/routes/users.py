from flask import Blueprint, request, jsonify
from app.services.api_services.users import get_users, add_user, delete_user, change_user
from flask_jwt_extended import jwt_required
from app.routes import role_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=(['GET', 'POST']))
@jwt_required()
@role_required('admin')
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
