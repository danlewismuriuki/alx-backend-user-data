#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from flask import jsonify, Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    """
    Handle GET requests to the root URL.

    Returns:
        A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
