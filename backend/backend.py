from flask import Flask
from registration import register_blueprint

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world"


app.register_blueprint(register_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
