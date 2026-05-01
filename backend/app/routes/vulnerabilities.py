from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.api_services.vulnerabilities import get_vulnerabilities_by_component

vulnerabilities_bp = Blueprint('vulnerabilities', __name__)


@vulnerabilities_bp.route('/vulnerabilities', methods=['GET'])
@jwt_required()
def vulnerabilities():
    id = request.args.get('component_id')
    result = get_vulnerabilities_by_component(id)
    return jsonify(result)
