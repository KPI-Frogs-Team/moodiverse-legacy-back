from datetime import datetime

from src.config import engine
from src.models.database import User, Avatar

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

def check_email_and_username(email, username):
    with Session(engine) as session:
        exists = session.query(User).filter((User.email == email) | (User.username == username)).first()
        return True if exists else False


def add_user_into_db(username, email, hashed_password, birthdate, registration_date):
    with Session(engine) as session:
        random_avatar_id = session.query(Avatar.id).order_by(func.random()).limit(1).one()[0]

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            birth_date=datetime.strptime(birthdate, '%d.%m.%Y'),
            registration_date=datetime.strptime(registration_date, '%d.%m.%Y'),
            avatar_id=random_avatar_id
        )

        session.add(user)
        session.commit()
