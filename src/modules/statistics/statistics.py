from src.config import app, rate_limits
from .functions import token_required, get_user_id, get_records_points, get_records_count
from .handlers import ratelimit_handler

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

statistics_blueprint = Blueprint('statistics', __name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app=app, key_func=get_remote_address)


@statistics_blueprint.route('/statistics/table', methods=['GET'])
@limiter.limit(rate_limits["default"])
@token_required
def get_table_statistics(decoded_token):
    username = decoded_token['user']

    month = request.json.get('month')
    if not month:
        return jsonify({'error': 'month field is required.'}), 400

    year = request.json.get('year')
    if not year:
        return jsonify({'error': 'year field is required.'}), 400

    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    try:
        records = get_records_points(user_id, month, year)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    if records:
        return records, 200

    return jsonify({'error': 'There\'s no records for this period of time.'}), 404


@statistics_blueprint.route('/statistics/round', methods=['GET'])
@limiter.limit(rate_limits["default"])
@token_required
def get_round_statistics(decoded_token):

    username = decoded_token['user']

    month = request.json.get('month')
    if not month:
        return jsonify({'error': 'month field is required.'}), 400

    year = request.json.get('year')
    if not year:
        return jsonify({'error': 'year field is required.'}), 400


    user_id = get_user_id(username)
    if not user_id:
        return jsonify({'error': 'User not found.'}), 404

    try:
        records = get_records_count(user_id, month, year)
    except:
        return jsonify({'error': 'Error occurred.'}), 500

    if records:
        return records, 200

    return jsonify({'error': 'There\'s no records for this period of time.'}), 404