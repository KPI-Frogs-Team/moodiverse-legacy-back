import jwt
from flask import jsonify, request
from functools import wraps
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import exists

from src.config import app
from src.config import engine
from src.models.database import User, Avatar


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


def get_avatar_and_username(username):
    with Session(engine) as session:
        user_query = (
            session.query(User.username, Avatar.avatar)
                .join(Avatar, User.avatar_id == Avatar.id)
                .where(User.username == username)
        )
        result = user_query.all()[0]
        result_json = {"username": result[0], "avatar": result[1]}

        return result_json


def check_user(username):
    with Session(engine) as session:
        is_exists = session.query(User).filter(User.username == username).first()
        return True if is_exists else False