from flask import Blueprint, current_app, request, jsonify, send_file, abort

from app.services.api_services.binary import get_binary_info, build_executable_module

binary_bp = Blueprint('binary', __name__)


@binary_bp.route('/binary', methods=['GET', 'POST'])
def binary():
    if request.method == 'GET':
        if request.args.get('action') == 'get_info':
            return jsonify(get_binary_info())
        if request.args.get('action') == 'get_file':
            try:
                file_path = '/home/user/VulnScanC/backend/binary/executable_module'
                return send_file(file_path, as_attachment=True)
            except FileNotFoundError as exc:
                current_app.logger.exception(
                    f'Executable module not found: {exc}')
                abort(404, description="Executable module not found")

    if request.method == 'POST':
        data = request.json
        if data['action'] == 'build_binary':
            build_executable_module()
            current_app.logger.info(f"Executable module has been built")
            return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
