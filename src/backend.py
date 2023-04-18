from config import app

from src.modules.register.registration import register_blueprint
from src.modules.retrieve_user_data.registration import register_blueprint_retrieve_user_account


@app.route('/')
def index():
    return "Hello world"


app.register_blueprint(register_blueprint)
app.register_blueprint(register_blueprint_retrieve_user_account)


if __name__ == "__main__":
    app.run(debug=True)
