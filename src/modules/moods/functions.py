from sqlalchemy.orm import Session

from src.config import engine
from src.models.database import Mood


def get_moods_from_db():
    with Session(engine) as session:
        moods = session.query(Mood).all()

        json_result = {
            'moods': [{'mood_id': mood.id, 'image': mood.image} for mood in moods]
        }

        return json_result
