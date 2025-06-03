from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.api_services.licenses import check_licenses, add_license, delete_license

licenses_bp = Blueprint('licenses', __name__)


@licenses_bp.route('/licenses', methods=(['POST']))
@jwt_required()
def licenses():
    data = request.json
    if data['action'] == 'check_licenses':
        check_licenses(data['project_id'])
    if data['action'] == 'add':
        add_license(data['component_id'], data['key'],
                    data['name'], data['spdx_id'], data['url'])
    if data['action'] == 'delete':
        delete_license(data['license_id'])
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
