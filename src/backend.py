from config import app

from src.modules.register.registration import register_blueprint
from src.modules.login.login import login_blueprint
from src.modules.records.records import record_blueprint


@app.route('/')
def index():
    return "Hello world"


app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(record_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
