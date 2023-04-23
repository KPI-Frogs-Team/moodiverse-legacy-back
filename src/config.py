from src.sensitive import database_path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_path

db = SQLAlchemy(app)
engine = create_engine(database_path)

rate_limits = {
    "default": "6 per minute"
}
