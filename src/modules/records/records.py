import datetime

from src.config import app, rate_limits
from .functions import token_required, get_user_id, create_mood_record, get_record_from_db, update_record_in_db, check_date
from .handlers import ratelimit_handler

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

record_blueprint = Blueprint('record', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@record_blueprint.route('/record', methods=['POST'])
@limiter.limit(rate_limits["default"])
@token_required
def create_record(decoded_token):
    username = decoded_token['user']

    mood_id = request.json.get('mood_id')
    text = request.json.get('text')
    try:
        date = datetime.datetime.strptime(request.json.get('date'), '%d.%m.%Y').date()
    except:
        return jsonify({'error': 'Error parsing a date.'}), 500
    if not mood_id or not text or not date:
        return jsonify({'error': 'Mood id, text and date fields are required.'}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    is_record_exists = check_date(user_id, date)
    if is_record_exists:
        return jsonify({'error': 'Record already exists at this date.'}), 500

    try:
        create_mood_record(user_id, mood_id, text, date)
    except:
        return jsonify({'error': 'Error occurred while creating record.'}), 500

    return '', 200


@record_blueprint.route('/record', methods=['GET'])
@limiter.limit(rate_limits["default"])
@token_required
def get_record(decoded_token):
    username = decoded_token['user']

    try:
        date_str = request.json.get('date')
        if not date_str:
            return jsonify({'error': 'Date field is required.'}), 400

        date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
    except:
        return jsonify({'error': 'Error parsing the date.'}), 500

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    record = get_record_from_db(user_id, date)

    if record:
        return record, 200

    return jsonify({'error': 'There\'s no record for this date.'}), 404


@record_blueprint.route('/record', methods=['PUT'])
@limiter.limit(rate_limits["default"])
@token_required
def update_record(decoded_token):
    username = decoded_token['user']

    new_mood_id = request.json.get('newMood_id')
    new_text = request.json.get('newText')
    try:
        date_str = request.json.get('date')
        if not date_str:
            return jsonify({'error': 'Date field is required.'}), 400

        date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
    except:
        return jsonify({'error': 'Error parsing the date.'}), 500
    if not new_mood_id or not new_text or not date:
        return jsonify({'error': 'newMood id, newText and date fields are required.'}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404
    is_date_exists = check_date(user_id, date)
    if not is_date_exists:
        return jsonify({'error': 'There\'s no record for this date.'}), 404

    update_record_in_db(user_id, date, new_mood_id, new_text)

    return '', 200
