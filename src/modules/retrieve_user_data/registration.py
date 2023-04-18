from src.config import app, rate_limits
from src.sensitive import connection
from .functions import retrieve_user
from .handlers import ratelimit_handler

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

register_blueprint_retrieve_user_account = Blueprint('user', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@register_blueprint_retrieve_user_account.route('/user/<userId>', methods=['GET'])
@limiter.limit(rate_limits["default"])
def retrieve_user_data(userId):
    user_id = userId
    try:
        data = retrieve_user(user_id)
        return jsonify({'user': {'id': data[0], 'username': data[1], 'first_name': data[2], 'last_name': data[3], 'e-mail': data[4], 'birthday': data[5], 'sex': data[6]}})
    except:
        return jsonify({"error": "Bad request"}), 400
