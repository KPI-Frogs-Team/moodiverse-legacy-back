from flask import jsonify, request
import jwt
from functools import wraps
from src.config import app
from src.models.database import User
from sqlalchemy.orm import Session
from src.config import engine


def check_user(username, password):
    with Session(engine) as session:
        exists = session.query(User).filter(User.username == username, User.password == password).first()
        return True if exists else False


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
