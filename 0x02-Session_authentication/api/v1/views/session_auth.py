#!/usr/bin/env python3
'''session authentication routes'''
from api.v1.views import app_views
from flask import jsonify, request, session
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''login user'''
    email = request.form.get('email')
    passwd = request.form.get('password')

    if not email:
        return jsonify({"error": 'email missing'}), 400

    if not passwd:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]

    if not user.is_valid_password(passwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    session_name = os.getenv('SESSION_NAME')
    res = jsonify(user.to_json())
    res.set_cookie(session_name, session_id)

    return res
