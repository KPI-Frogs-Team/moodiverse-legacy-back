import jwt
from flask import jsonify, request
from functools import wraps
from sqlalchemy.orm import Session

from src.config import app
from src.config import engine
from src.models.database import User


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


def compare_passwords(bcrypt, username, password):
    with Session(engine) as session:
        hashed_password = session.query(User).filter(User.username == username).first().password
        is_matched = bcrypt.check_password_hash(hashed_password, password)

        return is_matched


def delete_user_from_db(username):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
