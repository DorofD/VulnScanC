from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from app.services.api_services.sarif import upload_sarif, get_sarif_path, get_sarif_filenames, delete_sarif

sarif_bp = Blueprint('sarif', __name__)


@sarif_bp.route('/sarif', methods=(['GET', 'POST']))
@jwt_required()
def sarif():
    if request.method == 'GET':
        if request.args.get('action') == 'get_filenames':
            return get_sarif_filenames()
        if request.args.get('action') == 'get_file':
            return send_file(get_sarif_path(request.args.get('filename')), as_attachment=True)
    if request.method == 'POST':
        if 'file' in request.files and 'action' in request.form:
            file = request.files['file']
            action = request.form['action']
            project_name = request.form.get('project_name')
            if action == 'upload':
                filename = upload_sarif(file, project_name)
                if type(filename) == str:
                    return jsonify({'success': True, 'message': f"File {filename} uploaded successfully"}), 200
                return jsonify({'success': False, 'message': f"File not uploaded for project {project_name}"}), 400
        data = request.json
        if data['action'] == 'delete':
            delete_sarif(data['filename'])
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
