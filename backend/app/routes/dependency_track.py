from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from app.services.api_services.dependency_track import get_projects as get_dt_projects, get_components as get_dt_components

dependency_track_bp = Blueprint('dependency_track', __name__)


@dependency_track_bp.route('/dependency_track', methods=(['GET']))
@jwt_required()
def dependency_track():
    if request.args.get('action') == 'get_projects':
        result = get_dt_projects()
        return jsonify(result)

    if request.args.get('action') == 'get_components':
        result = get_dt_components(request.args.get('project_uuid'))
        return jsonify(result)
