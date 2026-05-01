from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.api_services.components import get_project_components, change_component_status

components_bp = Blueprint('components', __name__)


@components_bp.route('/components', methods=['GET', 'POST'])
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
