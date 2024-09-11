#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from flask import jsonify, Flask, request, make_response, abort
from auth import Auth
# from typing import bool
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
def users() -> str:
    """ask, you will
    implement the end-point to register a user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 200


@app.route('/sessions', methods=['POST'])
def login():
    """Log in a user and create a session."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)

    response = make_response(
        jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
