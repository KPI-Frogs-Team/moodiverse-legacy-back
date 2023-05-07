from src.config import app, rate_limits
from .functions import token_required, compare_passwords, delete_user_from_db
from .handlers import ratelimit_handler

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

user_blueprint = Blueprint('user', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@user_blueprint.route('/settings', methods=['DELETE'])
@limiter.limit(rate_limits["default"])
@token_required
def delete_user(decoded_token):
    username = decoded_token['user']

    password = request.json.get('password')
    if not password:
        return jsonify({'error': 'Password field is required.'}), 400

    if not compare_passwords(bcrypt, username, password):
        return jsonify({'error': 'Wrong password'}), 403

    try:
        delete_user_from_db(username)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    return '', 200
