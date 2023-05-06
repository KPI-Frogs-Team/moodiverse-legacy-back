from src.config import app, rate_limits
from .functions import get_moods_from_db
from .handlers import ratelimit_handler

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

moods_blueprint = Blueprint('moods', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@moods_blueprint.route('/moods', methods=['GET'])
@limiter.limit(rate_limits["default"])
def get_moods():
    try:
        moods = get_moods_from_db()
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    return moods, 200
