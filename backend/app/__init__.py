from flask import Flask, jsonify, current_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
import os
import logging
import traceback
from datetime import timedelta
from dotenv import load_dotenv

from app.repository.db_model import create_db
from app.services.api_services.users import add_user_db, get_users


def create_app():
    load_dotenv('.env')
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
    app.config["JWT_TOKEN_LOCATION"] = ['headers', 'cookies']
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = ""
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=180)
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'

    jwt = JWTManager()
    jwt.init_app(app)

    @app.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(e):
        return jsonify({"msg": "Missing Authorization Header"}), 401

    @app.errorhandler(Exception)
    def handle_value_error(error):
        print(f"ERROR: {error}")
        traceback.print_exc()
        current_app.logger.exception(
            f'Backend has unknown error: {error}')
        return jsonify({'error': f'Backend error: {error}'}), 500

    handler = logging.FileHandler('data/app.log')
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.logger.handlers = []
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    from app.routes.base_routes import main as main_blueprint
    from app.routes.login import login_bp
    from app.routes.users import users_bp
    from app.routes.logs import logs_bp
    from app.routes.bitbake import bitbake_bp
    from app.routes.reports import reports_bp
    from app.routes.sarif import sarif_bp
    from app.routes.svacer import svacer_bp
    from app.routes.dependency_track import dependency_track_bp
    from app.routes.bdu import bdu_bp
    from app.routes.licenses import licenses_bp
    from app.routes.snapshots import snapshots_bp

    app.register_blueprint(main_blueprint)
    app.register_blueprint(login_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(bitbake_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(sarif_bp)
    app.register_blueprint(svacer_bp)
    app.register_blueprint(dependency_track_bp)
    app.register_blueprint(bdu_bp)
    app.register_blueprint(licenses_bp)
    app.register_blueprint(snapshots_bp)
    print(app.url_map)
    create_db()
    users = get_users()
    if not users:
        add_user_db('admin', 'local', 'admin', 'admin')

    return app
