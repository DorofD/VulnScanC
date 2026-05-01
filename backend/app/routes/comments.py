from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.api_services.component_comments import get_comments_for_component, add_comment_for_component, delete_component_comment

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/comments', methods=['GET', 'POST'])
@jwt_required()
def comments():
    if request.method == 'GET':
        if request.args.get('type') == 'component':
            result = get_comments_for_component(
                request.args.get('component_id'))
            return jsonify(list(reversed(result)))
        if request.args.get('type') == 'vuln':
            pass

    if request.method == 'POST':
        data = request.json
        if data['action'] == 'add':
            if data['type'] == 'component':
                add_comment_for_component(
                    data['user_id'], data['component_id'], data['comment'])
                if data['type'] == 'vuln':
                    pass
        if data['action'] == 'delete':
            if data['type'] == 'component':
                delete_component_comment(data['comment_id'])
            if data['type'] == 'vuln':
                pass
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
