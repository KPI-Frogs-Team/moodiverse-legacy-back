from src.sensitive import database_path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
db = SQLAlchemy(app)

moods = Table('moods', db.metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(255), nullable=False),
              Column('image', String(255), nullable=False),
              Column('points', Integer, nullable=False),
              )

avatars = Table('avatars', db.metadata,
                Column('id', Integer, primary_key=True),
                Column('avatar', String(255), nullable=False)
                )

sex = Table('sex', db.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(255), nullable=False)
            )

user = Table('user', db.metadata,
             Column('id', Integer, primary_key=True),
             Column('username', String(255), nullable=False),
             Column('first_name', String(255)),
             Column('last_name', String(255)),
             Column('email', String(255), nullable=False),
             Column('password', String(255), nullable=False),
             Column('birth_date', db.Date),
             Column('sex_id', Integer, ForeignKey('sex.id')),
             Column('registration_date', db.Date, nullable=False),
             Column('avatar_id', Integer, ForeignKey('avatars.id')),
             )

records = Table('records', db.metadata,
                Column('id', Integer, primary_key=True),
                Column('date', db.Date, nullable=False),
                Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                Column('mood_id', Integer, ForeignKey('moods.id'), nullable=False),
                Column('text', db.Text),
                )


class Mood(db.Model):
    __table__ = moods


class Avatar(db.Model):
    __table__ = avatars


class Sex(db.Model):
    __table__ = sex


class User(db.Model):
    __table__ = user


class Record(db.Model):
    __table__ = records
