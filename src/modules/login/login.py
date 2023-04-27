from flask import session
import jwt
from datetime import datetime
from src.config import app, rate_limits
from src.modules.login.functions import check_user, compare_passwords
from src.modules.login.handlers import ratelimit_handler

from src.config import login_token_lifetime

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

login_blueprint = Blueprint('login', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@login_blueprint.route('/login', methods=['POST'])
@limiter.limit(rate_limits["default"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if check_user(username) and compare_passwords(bcrypt, username, password):
        session['logged_in'] = True

        token = jwt.encode({
            'user': request.json.get('username'),
            'expiration': str(datetime.utcnow() + login_token_lifetime)
        },
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Unable to verify a user'}), 403
