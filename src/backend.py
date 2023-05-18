from config import app

from src.modules.register.registration import register_blueprint
from src.modules.login.login import login_blueprint
from src.modules.records.records import record_blueprint
from src.modules.moods.moods import moods_blueprint
from src.modules.statistics.statistics import statistics_blueprint
from src.modules.data.data import data_blueprint
from src.modules.avatars.avatars import avatars_blueprint
from src.modules.user.user import user_blueprint


@app.route('/')
def index():
    return "Hello world"


app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(record_blueprint)
app.register_blueprint(moods_blueprint)
app.register_blueprint(statistics_blueprint)
app.register_blueprint(data_blueprint)
app.register_blueprint(avatars_blueprint)
app.register_blueprint(user_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
