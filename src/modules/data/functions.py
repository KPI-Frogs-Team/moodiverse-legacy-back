import jwt
from flask import jsonify, request
from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from src.config import app
from src.config import engine
from src.models.database import User, Sex


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


def get_user_id(username):
    with Session(engine) as session:
        user_id = session.query(User.id).filter_by(username=username).first()[0]

        return user_id


def get_user_data(user_id):
    with Session(engine) as session:
        is_exists = session.query(exists().where((User.sex_id != None) & (User.id == user_id))).scalar()

        if is_exists:
            query = session.query(User.username, User.first_name, User.last_name, User.birth_date,
                                  Sex.name.label('sex_name')).join(Sex, Sex.id == User.sex_id).filter(User.id == user_id).all()
            if len(query) > 0:
                result = query[0]
                json_result = {
                    "Username": result.username if result.username else "",
                    "FirstName": result.first_name if result.first_name else "",
                    "LastName": result.last_name if result.last_name else "",
                    "Birthdate": result.birth_date.strftime("%d.%m.%Y") if result.birth_date else "",
                    "Sex": result.sex_name if result.sex_name else ""
                }

        else:
            query = session.query(User.username, User.first_name, User.last_name, User.birth_date).filter(User.id == user_id).all()
            if len(query) > 0:
                result = query[0]
                json_result = {
                    "Username": result.username if result.username else "",
                    "FirstName": result.first_name if result.first_name else "",
                    "LastName": result.last_name if result.last_name else "",
                    "Birthdate": result.birth_date.strftime("%d.%m.%Y") if result.birth_date else "",
                    "Sex": ""
                }

        return json_result


def change_password(user_id, hashed_password):
    with Session(engine) as session:
        session.query(User).filter_by(id=user_id).update(
            {'password': hashed_password}
        )
        session.commit()


def change_email(user_id, new_email):
    with Session(engine) as session:
        session.query(User).filter_by(id=user_id).update(
            {'email': new_email}
        )
        session.commit()


def change_data(user_id, newUsername, newFirstName, newLastName, newBirthdate, newSex_id):
    with Session(engine) as session:
        if newUsername:
            session.query(User).filter_by(id=user_id).update(
                {'username': newUsername}
            )
        if newFirstName:
            session.query(User).filter_by(id=user_id).update(
                {'first_name': newFirstName}
            )
        if newLastName:
            session.query(User).filter_by(id=user_id).update(
                {'last_name': newLastName}
            )
        if newBirthdate:
            session.query(User).filter_by(id=user_id).update(
                {'birth_date': newBirthdate}
            )
        if newSex_id:
            session.query(User).filter_by(id=user_id).update(
                {'sex_id': newSex_id}
            )

        session.commit()

