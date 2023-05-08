from src.config import app, rate_limits
from .functions import token_required, get_avatar_and_username, check_user, get_random_avatar, set_avatar
from .handlers import ratelimit_handler

from flask import Blueprint, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

avatars_blueprint = Blueprint('avatar', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@avatars_blueprint.route('/user/header', methods=['GET'])
@limiter.limit(rate_limits["default"])
@token_required
def get_header(decoded_token):
    username = decoded_token['user']

    if not check_user(username):
        return jsonify({'error': 'Unable to verify a user'}), 403

    try:
        avatar_and_username = get_avatar_and_username(username)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    return avatar_and_username, 200


@avatars_blueprint.route('/avatar', methods=['GET'])
@limiter.limit(rate_limits["default"])
@token_required
def get_avatar(decoded_token):
    username = decoded_token['user']
    if not check_user(username):
        return jsonify({'error': 'Unable to verify a user'}), 403

    try:
        avatar = get_random_avatar()
        set_avatar(username, avatar[0])
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    return avatar[1], 200
