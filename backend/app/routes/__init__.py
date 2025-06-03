from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt


def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt_data = get_jwt()
            if jwt_data.get('role') != required_role:
                return jsonify({"msg": "Unauthorized"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
