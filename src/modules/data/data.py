from src.config import app, rate_limits
from .functions import token_required, get_user_id, get_user_data
from .handlers import ratelimit_handler

from flask import Blueprint, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

data_blueprint = Blueprint('data', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@data_blueprint.route('/user/getPersonalData', methods=['GET'])
@limiter.limit(rate_limits["default"])
@token_required
def get_record(decoded_token):
    username = decoded_token['user']


    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User field is required.'}), 404

    try:
        record = get_user_data(user_id)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    if record:
        return record, 200

    return jsonify({'error': 'There\'s no data.'}), 404
