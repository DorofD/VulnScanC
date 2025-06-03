from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.api_services.svacer import get_projects as get_svacer_projects, get_snapshots as get_svacer_snapshots

svacer_bp = Blueprint('svacer', __name__)


@svacer_bp.route('/svacer', methods=(['GET']))
@jwt_required()
def svacer():
    if request.args.get('action') == 'get_projects':
        result = get_svacer_projects()
        return jsonify(result)

    if request.args.get('action') == 'get_snapshots':
        result = get_svacer_snapshots(request.args.get(
            'project_id'), request.args.get('branch_id'))
        return jsonify(result)
