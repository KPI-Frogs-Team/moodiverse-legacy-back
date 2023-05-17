import datetime

from src.config import app, rate_limits
from .functions import token_required, get_user_id, get_user_data
from .handlers import ratelimit_handler

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

user_blueprint = Blueprint('data', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)



@user_blueprint.route('/user/getPersonalData', methods=['GET'])
@limiter.limit(rate_limits["default"])
@token_required
def get_record(decoded_token):
    username = decoded_token['user']


    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    record = get_user_data(user_id)

    if record:
        return record, 200

    return jsonify({'error': 'There\'s no data.'}), 404

