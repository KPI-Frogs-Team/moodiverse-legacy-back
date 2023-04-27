from src.config import app

from flask import jsonify


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "You've been rate limited. Wait a minute."}), 429
