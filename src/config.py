from flask import Flask

# Flask app
app = Flask(__name__)

# Dict with rate limits
rate_limits = {
    "default": "6 per minute"
}
