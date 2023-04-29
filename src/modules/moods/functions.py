from sqlalchemy.orm import Session

from src.config import engine
from src.models.database import Mood

def get_moods_from_db():
    with Session(engine) as session:
        moods = session.query(Mood).all()

        result = []
        for mood in moods:
            result.append({
                'name': mood.name,
                'image': mood.image
            })

        json_result = {
            'moods': result
        }

        return json_result
