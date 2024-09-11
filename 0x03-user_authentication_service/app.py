#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from flask import jsonify, Flask, request
from auth import Auth
app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world():
    """
    Handle GET requests to the root URL.

    Returns:
        A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ask, you will
    implement the end-point to register a user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or password:
        return jsonify({"message": "email and password are required"}), 400
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "{user.email} already reegistered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
