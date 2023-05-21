from src.config import app, rate_limits
from datetime import datetime
from src.config import login_token_lifetime
from .functions import token_required, get_user_id, get_user_data, compare_passwords, change_password, change_email, change_data
from .handlers import ratelimit_handler
import jwt
from flask import Blueprint, jsonify
from flask_bcrypt import Bcrypt
from flask import jsonify, request
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


@data_blueprint.route('/user/updateUserPasswordRequest', methods=['PUT'])
@limiter.limit(rate_limits["default"])
@token_required
def updateUserPasswordRequest(decoded_token):
    username = decoded_token['user']

    oldPassword = request.json.get('oldPassword')
    newPassword = request.json.get('newPassword')

    if not oldPassword:
        return jsonify({'error': 'oldPassword field is required.'}), 404

    if not newPassword:
        return jsonify({'error': 'newPassword field is required.'}), 404

    if not compare_passwords(bcrypt, username, oldPassword):
        return jsonify({'error': 'Password mismatch.'}), 500

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404
    hashed_password = bcrypt.generate_password_hash(newPassword).decode('utf-8')
    try:
        change_password(user_id, hashed_password)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    return '', 200


@data_blueprint.route('/user/updateUserEmailRequest', methods=['PUT'])
@limiter.limit(rate_limits["default"])
@token_required
def updateUserEmailRequest(decoded_token):
    username = decoded_token['user']

    email = request.json.get('newEmail')

    if not email:
        return jsonify({'error': 'email field is required.'}), 404

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    try:
        change_email(user_id, email)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    return '', 200


@data_blueprint.route('/user/updateUserPersonalDataRequest', methods=['PUT'])
@limiter.limit(rate_limits["default"])
@token_required
def updateUserPersonalDataRequest(decoded_token):
    username = decoded_token['user']

    newUsername = request.json.get('newUsername')
    newFirstName = request.json.get('newFirstName')
    newLastName = request.json.get('newLastName')
    newBirthdate = request.json.get('newBirthdate')
    newSex = request.json.get('newSex')

    user_id = get_user_id(username)

    if newUsername:
        username = newUsername

    token = jwt.encode({
        'user': username,
        'expiration': str(datetime.utcnow() + login_token_lifetime)
    },
        app.config['SECRET_KEY'], algorithm="HS256")

    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    try:
        change_data(user_id, newUsername, newFirstName, newLastName, newBirthdate, newSex)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    return jsonify({'token': token})
