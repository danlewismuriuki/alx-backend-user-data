#!/usr/bin/env python3
""" Module of Session authentication views
"""
# from api.v1.views import app_views
from flask import Blueprint, request, jsonify
from models.user import User
import os

session_auth_bp = Blueprint(
    'session_auth_bp', __name__)


@session_auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles user login and session creation.

    Args:
        None

    Returns:
        JSON: {
            "error": "email missing" | "password missing" | 
                     "no user found for this email" | 
                     "wrong password" | 
                     User information
        }
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 400

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())

    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
