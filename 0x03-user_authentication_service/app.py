#!/usr/bin/env python3
'''flask web application instance and route'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    '''welcome route'''
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def sign_up() -> str:
    '''register user'''
    email = request.form.get('email')
    passwd = request.form.get('password')

    if not (email and passwd):
        return jsonify({"error": "email and password is required"}), 400

    try:
        auth.register_user(email, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 201


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''validate user credentials and
        create a session add it to cookie with session_id key
    '''
    email = request.form.get('email')
    passwd = request.form.get('password')

    if not (email and passwd):
        return jsonify({"error": "email and password is required"}), 400

    if not auth.valid_login(email, passwd):
        abort(401)

    session_id = auth.create_session(email)
    response = jsonify({"email": "<user email>", "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    '''destroy user session'''
    session_id = request.cookies.get("session_id")

    user = auth.get_user_from_session_id(session_id)
    if not user:
        return abort(403)

    auth.destroy_session(user.id)

    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
