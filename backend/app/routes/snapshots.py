from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.api_services.snapshots import get_project_snapshots, delete_snapshot, get_bitbake_project_snapshots, delete_bitbake_snapshot

snapshots_bp = Blueprint('snapshots', __name__)


@snapshots_bp.route('/snapshots', methods=(['GET', 'POST']))
@jwt_required()
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
