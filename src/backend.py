from config import app

from src.modules.register.registration import register_blueprint


@app.route('/')
def index():
    return "Hello world"


app.register_blueprint(register_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
