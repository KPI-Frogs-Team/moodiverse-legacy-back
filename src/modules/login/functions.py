from src.models.database import User
from sqlalchemy.orm import Session
from src.config import engine


def check_user(username):
    with Session(engine) as session:
        is_exists = session.query(User).filter(User.username == username).first()
        return True if is_exists else False


def compare_passwords(bcrypt, username, password):
    with Session(engine) as session:
        hashed_password = session.query(User).filter(User.username == username).first().password
        is_matched = bcrypt.check_password_hash(hashed_password, password)

        return is_matched
