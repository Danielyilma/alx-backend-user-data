#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = {
    'auth': Auth,
    'basic_auth': BasicAuth,
    'session_auth': SessionAuth,
    'session_exp_auth': SessionExpAuth,
    'session_db_auth': SessionDBAuth
}

a_type = os.getenv('AUTH_TYPE')

if a_type:
    auth = auth_type.get(a_type, None)()


@app.before_request
def auth_user() -> None:
    '''checking if routes need authentication
    and user is authenticated'''
    if not auth:
        return

    if not auth.require_auth(request.path, [
        '/api/v1/status/', '/api/v1/unauthorized/',
        '/api/v1/forbidden/', '/api/v1/auth_session/login/'
    ]):
        return None

    auth_header = auth.authorization_header(request)
    sess_cookie = auth.session_cookie(request)

    if not auth_header and not sess_cookie:
        abort(401)

    user = auth.current_user(request)
    if not user:
        abort(403)

    request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbiddern(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
