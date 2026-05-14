from flask import Blueprint, request, jsonify, current_app

from app.services.api_services.save_hashes import SaveHashesService

save_hashes_bp = Blueprint('save_hashes', __name__)


@save_hashes_bp.route('/save_hashes', methods=['POST'])
def save_hashes():
    try:
        data = request.get_json()
        required_fields = ['project_name', 'datetime', 'hashes']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        process = data.get('process', False)
        if process:
            result = SaveHashesService().save_hashes(data)
            current_app.logger.info(
                f"Hashes received and processed for project: {data['project_name']} Time: {data['datetime']}")

            return jsonify({
                "message": "Hashes saved and processed successfully",
                "file_path": result
            }), 200
        else:
            result = SaveHashesService().save_hashes_only(data)
            current_app.logger.info(
                f"Hashes received and saved for project: {data['project_name']} Time: {data['datetime']}")

            return jsonify({
                "message": "Hashes saved successfully",
                "file_path": result
            }), 200

    except FileNotFoundError as exc:
        current_app.logger.exception(
            f"Error when handling save_hashes: {exc}")
        return jsonify({"error": "Hashes file not found"}), 404
    except Exception as exc:
        current_app.logger.exception(
            f"Error when handling save_hashes: {exc}")
        return jsonify({"error": str(exc)}), 500


@save_hashes_bp.route('/trigger_osv_scan', methods=['POST'])
def trigger_osv_scan():
    try:
        data = request.get_json()
        required_fields = ['project_name', 'datetime']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        project_name = data['project_name']
        datetime_str = data['datetime']

        result = SaveHashesService().trigger_scan(project_name, datetime_str)
        current_app.logger.info(
            f"OSV scan triggered for project: {project_name} Time: {datetime_str}")

        return jsonify({
            "message": "OSV scan completed successfully"
        }), 200

    except FileNotFoundError as exc:
        current_app.logger.exception(
            f"Error when triggering OSV scan: {exc}")
        return jsonify({"error": "Hashes file not found"}), 404
    except Exception as exc:
        current_app.logger.exception(
            f"Error when triggering OSV scan: {exc}")
        return jsonify({"error": str(exc)}), 500
