from config import app
from sensitive import connection

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

register_blueprint = Blueprint('register', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@register_blueprint.route('/register', methods=['POST'])
@limiter.limit("6 per minute")
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    birthdate = request.json.get('birthdate')

    if not username or not email or not password or not birthdate:
        return jsonify({'error': 'Missing required fields'}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    with connection.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO "user" (username, email, password, birth_date, sex_id) VALUES (%s, %s, %s, %s, NULL);''',
            (username, email, hashed_password, birthdate))
        connection.commit()

    return jsonify({'response': 'User created successfully!'}), 200


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="You've been rate limited. Wait a minute."), 429
