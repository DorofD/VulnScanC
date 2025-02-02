import logging
from flask import Flask
from flask_cors import CORS
from app.repository.db_model import create_db
from app.services.api_services.users import add_user_db, get_users


def create_app():
    app = Flask(__name__)
    CORS(app, expose_headers=['Content-Disposition'])
    app.config['SECRET_KEY'] = 'dfgjnldfkjgnsladkfjn1488'
    app.config['CORS_HEADERS'] = 'Content-Type'
    handler = logging.FileHandler('data/app.log')
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.logger.handlers = []
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    create_db()
    users = get_users()
    if not users:
        add_user_db('admin', 'local', 'admin', 'admin')

    return app
