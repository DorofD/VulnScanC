from flask import Blueprint, request, jsonify, abort, current_app

from app.services.search_data.search_data import SearchDataService

search_data_bp = Blueprint('search_data', __name__)


@search_data_bp.route('/search_data', methods=['POST'])
def search_data():
    try:
        data = request.get_json()
        if data['status'] == 'ok':
            SearchDataService().save_search_data(data)
            current_app.logger.info(
                f"Data received from Executable Module, the processing was successful! Project: {data['project_name']} Time: {data['datetime']}")
        elif data['status'] == 'fail':
            current_app.logger.error(
                f"Executable Module could not collect the data for project: {data['project_name']}")
        response = {
            "message": "Data processed successfully"
        }
        return jsonify(response), 200

    except FileNotFoundError as exc:
        current_app.logger.exception(
            f"Error when handling search data from Executable Module: {exc}")
        abort(404, description="Error when handling search data")
