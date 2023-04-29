import datetime

from src.config import app, rate_limits
from .functions import token_required, get_mood_id, get_user_id, create_mood_record, create_response, get_record_from_db
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

    mood_name = request.json.get('mood')
    text = request.json.get('text')
    try:
        date = datetime.datetime.strptime(request.json.get('date'), '%d.%m.%Y').date()
    except:
        return jsonify({'error': 'Error parsing a date.'}), 500
    if not mood_name or not text or not date:
        return jsonify({'error': 'Mood, text and date fields are required.'}), 400

    mood_id = get_mood_id(mood_name)
    if not mood_id:
        return jsonify({'error': 'Mood not found.'}), 404

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    try:
        create_mood_record(user_id, mood_id, text, date)
    except:
        return jsonify({'error': 'Error occurred while creating record.'}), 500

    response = create_response()

    return response, 200


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
        return jsonify({'error': 'Error parsing the date.'}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    record = get_record_from_db(user_id, date)

    if record:
        return record, 200
    else:
        return jsonify({'error': 'There\'s no record for this date.'}), 404
