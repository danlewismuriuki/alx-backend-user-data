#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from models.user import User  # isort:skip
from api.v1.views.session_auth import session_auth_bp # isort:skip
from api.v1.views.users import *  # isort:skip
from api.v1.views.index import *  # isort:skip
from flask import Blueprint

app_views.register_blueprint(session_auth_bp, url_prefix='/auth_session')


# isort: on

# isort: off
# app_views.register_blueprint(session_auth_bp, url_prefix='/auth_session')
# from flask import Blueprint  # isort:skip

User.load_from_file()
