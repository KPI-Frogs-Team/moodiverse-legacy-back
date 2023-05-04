from datetime import date

from src.config import app, rate_limits
from .functions import check_email_and_username, add_user_into_db
from .handlers import ratelimit_handler

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

register_blueprint = Blueprint('register', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@register_blueprint.route('/user/register', methods=['POST'])
@limiter.limit(rate_limits["default"])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    birthdate = request.json.get('birthdate')
    registration_date = date.today().strftime('%d.%m.%Y')

    if not username or not email or not password or not birthdate or not registration_date:
        return jsonify({'error': 'Missing required fields'}), 400

    is_exists = check_email_and_username(email, username)

    if is_exists:
        return jsonify({'error': 'User with given email or username already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    add_user_into_db(username, email, hashed_password, birthdate, registration_date)

    return jsonify({'response': 'User created successfully!'}), 200
