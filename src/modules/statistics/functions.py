import jwt
from flask import jsonify, request
from functools import wraps

from sqlalchemy import func
from sqlalchemy.orm import Session
from calendar import monthrange

from src.config import app
from src.config import engine
from src.models.database import Mood, User, Record


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return func(decoded_token, *args, **kwargs)
        except:
            return func(decoded_token, *args, **kwargs)

    return decorated


def get_user_id(username):
    with Session(engine) as session:
        user_id = session.query(User.id).filter_by(username=username).first()[0]

        return user_id


def get_records_points(user_id, month, year):
    start_date = f'{year}-{month}-01'
    end_date = f'{year}-{month}-{monthrange(int(year), int(month))[1]}'
    with Session(engine) as session:
        records = session.query(Record.text, Mood.points, Record.date).join(Mood, Record.mood_id == Mood.id).filter(Record.user_id == user_id).filter(Record.date.between(start_date, end_date)).all()

        json_result = {
            'statistics': [{'date': record.date.strftime("%d.%m.%Y"), 'points': record.points} for record in records]
        }

        return json_result


def get_records_count(user_id, month, year):
    start_date = f'{year}-{month}-01'
    end_date = f'{year}-{month}-{monthrange(int(year), int(month))[1]}'
    with Session(engine) as session:
        records = session.query(Record.mood_id, Mood.image, func.count(Record.id)). \
            join(Mood, Record.mood_id == Mood.id). \
            filter(Record.user_id == user_id). \
            filter(Record.date.between(start_date, end_date)). \
            group_by(Record.mood_id, Mood.image).all()
        json_result = {
            'statistics': [{'image': record.image, 'count': record[2]} for record in records]
        }

        return json_result
