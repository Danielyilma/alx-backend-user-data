#!/usr/bin/env python3
'''flask web application instance and route'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    '''welcome route'''
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    '''register user'''
    email = request.form.get('email')
    passwd = request.form.get('password')

    if not (email and passwd):
        return jsonify({"error": "email and password is required"}), 400

    try:
        AUTH.register_user(email, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 200


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''validate user credentials and
        create a session add it to cookie with session_id key
    '''
    email = request.form.get('email')
    passwd = request.form.get('password')

    if not (email and passwd):
        return jsonify({"error": "email and password is required"}), 400

    if not AUTH.valid_login(email, passwd):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    '''destroy user session'''
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    '''return the user profile using session_id'''
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    '''create reset_password token'''
    email = request.form.get('email')

    if not email:
        abort(403)

    try:
        token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)

    return jsonify({"email": email, "reset_token": token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    '''update user password'''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not (email and reset_token and new_password):
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    return jsonify({
        "email": email, "message": "Password updated"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
