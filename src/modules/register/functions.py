from datetime import datetime

from src.config import engine
from src.models.database import User

from sqlalchemy.orm import Session


def check_email_and_username(email, username):
    with Session(engine) as session:
        exists = session.query(User).filter((User.email == email) | (User.username == username)).first()
        return True if exists else False


def add_user_into_db(username, email, hashed_password, birthdate, registration_date):
    with Session(engine) as session:
        user = User(
            username=username,
            email=email,
            password=hashed_password,
            birth_date=datetime.strptime(birthdate, '%d.%m.%Y'),
            registration_date=datetime.strptime(registration_date, '%d.%m.%Y')
        )

        session.add(user)
        session.commit()
