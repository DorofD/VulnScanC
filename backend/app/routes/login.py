import os
from dotenv import load_dotenv
from flask import Blueprint, current_app, request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies, jwt_required, get_jwt_identity, get_jwt
from app.services.api_services.users import signin

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=(['POST']))
def login():
    load_dotenv('.env')
    secure_cookie = os.environ['REFRESH_TOKEN_COOKIE_SECURE']
    if secure_cookie == 'False':
        secure_cookie = False
    else:
        secure_cookie = True

    user = request.json
    auth_result = signin(user['login'], user['password'])
    if auth_result:
        user_claims = {
            "role": auth_result['role']
        }
        access_token = create_access_token(
            identity=user['login'], additional_claims=user_claims)
        refresh_token = create_refresh_token(
            identity=user['login'], additional_claims=user_claims)
        current_app.logger.info(f"User is logged in: {user['login']}")

        response = jsonify(
            {'success': True, 'body': auth_result, 'access_token': access_token})

        response.set_cookie(  # поправить под http/https
            'refresh_token',
            refresh_token,
            httponly=secure_cookie,
            secure=secure_cookie,
            samesite='None',
        )
        return response, 200

    current_app.logger.error(f"User failed to log in: {user['login']}")
    return jsonify({'success': False}), 401


@login_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    print('refresh token')
    jwt_data = get_jwt()
    identity = get_jwt_identity()
    user_role = jwt_data.get('role')
    user_claims = {
        "role": user_role
    }
    new_access_token = create_access_token(
        identity=identity, additional_claims=user_claims)
    new_refresh_token = create_refresh_token(
        identity=identity, additional_claims=user_claims)

    response = jsonify({
        'success': True,
        'access_token': new_access_token
    })

    secure_cookie = os.environ['REFRESH_TOKEN_COOKIE_SECURE']
    if secure_cookie == 'False':
        secure_cookie = False
    else:
        secure_cookie = True

    response.set_cookie(  # поправить под http/https
        'refresh_token',
        new_refresh_token,
        httponly=secure_cookie,
        secure=secure_cookie,
        samesite='Strict',
    )

    return response, 200
