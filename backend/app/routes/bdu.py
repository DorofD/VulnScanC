from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from app.services.api_services.bdu import get_bdu_info, update_bdu, update_vulns_by_cve_id, get_component_bdu_vulns

bdu_bp = Blueprint('bdu', __name__)


@bdu_bp.route('/bdu', methods=(['GET', 'POST']))
@jwt_required()
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
