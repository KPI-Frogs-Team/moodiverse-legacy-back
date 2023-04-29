import jwt
from flask import jsonify, request
from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

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
            return jsonify({'Message': 'Invalid token'}), 403

    return decorated


def get_mood_id(name):
    with Session(engine) as session:
        mood_id = session.query(Mood.id).filter_by(name=name).first()[0]

        return mood_id


def get_user_id(username):
    with Session(engine) as session:
        user_id = session.query(User.id).filter_by(username=username).first()[0]

        return user_id


def create_mood_record(user_id, mood_id, text, date):
    with Session(engine) as session:
        record = Record(
            date=date,
            user_id=user_id,
            mood_id=mood_id,
            text=text
        )

        session.add(record)
        session.commit()


def create_response():
    with Session(engine) as session:
        moods = session.query(Mood).all()

        result = []
        for mood in moods:
            result.append({
                'name': mood.name,
                'image': mood.image
            })

        json_result = {
            'moods': result
        }

        return json_result


def get_record_from_db(user_id, date):
    with Session(engine) as session:
        query = session.query(Record.text, Mood.image).join(Mood, Record.mood_id == Mood.id).filter(Record.user_id == user_id, Record.date == date).all()

        if len(query) > 0:
            result = query[0]
            json_result = {"emoji": result[1], "text": result[0]}

            return json_result
        else:
            return None


def check_date(user_id, date):
    with Session(engine) as session:
        is_exists = session.query(exists().where((Record.user_id == user_id) & (Record.date == date))).scalar()

        return is_exists


def update_record_in_db(user_id, date, new_mood_id, new_text):
    with Session(engine) as session:
        session.query(Record).filter_by(user_id=user_id, date=date).update(
            {'mood_id': new_mood_id, 'text': new_text}
        )
        session.commit()
