from flask import Blueprint, request, jsonify, send_file, abort
from app.services.logs import get_logs, get_log_file_path, delete_logs
from flask_jwt_extended import jwt_required

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/logs', methods=(['GET', 'POST']))
@jwt_required()
def logs():
    if request.method == 'GET':
        if request.args.get('action') == 'get_json':
            result = get_logs()
            return jsonify(result)

        if request.args.get('action') == 'get_file':
            try:
                file_path = get_log_file_path()
                return send_file(file_path, as_attachment=True)
            except FileNotFoundError:
                abort(404, description="Log file not found")
    if request.method == 'POST':
        data = request.json
        if data['action'] == 'clear':
            delete_logs()
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}

# from flask import Blueprint, request, current_app, jsonify, send_file, abort
# from app.services.api_services.logs import get_logs
# from flask_jwt_extended import jwt_required

# logs_bp = Blueprint('logs', __name__)


# @logs_bp.route('/logs', methods=(['GET', 'POST']))
# @jwt_required()
# def logs():
#     if request.method == 'GET':
#         if request.args.get('action') == 'get_json':
#             result = get_logs()
#             return jsonify(result)

#         if request.args.get('action') == 'get_file':
#             try:
#                 import os
#                 file_path = os.path.join(os.getcwd(), 'data', 'app.log')
#                 return send_file(file_path, as_attachment=True)
#             except FileNotFoundError:
#                 abort(404, description="Log file not found")
