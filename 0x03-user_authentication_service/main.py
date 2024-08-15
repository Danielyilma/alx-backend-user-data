#!/usr/bin/env python3
'''end to end integration testing'''
import requests
import json


protocol = 'http://'
domain = 'localhost:'
port = '5000'


def register_user(email: str, password: str) -> None:
    'testing resgister user route'
    route = '/users'
    url = protocol + domain + port + route
    expected_response = {'email': email, "message": "user created"}

    response = requests.post(url, data={'email': email, 'password': password})

    assert response.status_code == 200
    assert expected_response == json.loads(response.text)


def log_in_wrong_password(email: str, password: str) -> None:
    '''testing login with wrong password'''
    route = '/sessions'
    url = protocol + domain + port + route

    response = requests.post(url, data={'email': email, 'password': password})

    assert response.status_code == 401


def profile_unlogged() -> None:
    '''testing profile route with out loging in'''
    route = '/profile'
    url = protocol + domain + port + route

    response = requests.get(url)

    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    '''testing login route'''
    route = '/sessions'
    url = protocol + domain + port + route
    expected_response = {"email": email, "message": "logged in"}

    response = requests.post(url, data={'email': email, 'password': password})

    assert response.status_code == 200
    assert json.loads(response.text) == expected_response

    return response.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    '''testing profile route with after loging in'''
    route = '/profile'
    url = protocol + domain + port + route
    expected_response = {"email": 'guillaume@holberton.io'}

    response = requests.get(url, cookies={'session_id': session_id})

    assert response.status_code == 200
    assert json.loads(response.text) == expected_response


def log_out(session_id: str) -> None:
    '''logout route'''
    route = '/sessions'
    url = protocol + domain + port + route
    expected_response = {"message": "Bienvenue"}

    response = requests.delete(url, cookies={'session_id': session_id})

    assert response.status_code == 200
    assert json.loads(response.text) == expected_response


def reset_password_token(email: str) -> str:
    '''testing reset password route'''
    route = '/reset_password'
    url = protocol + domain + port + route

    response = requests.post(url, data={'email': email})

    assert response.status_code == 200

    return json.loads(response.text).get('reset_token')


def update_password(email: str, reset_token: str, password: str) -> None:
    '''testing update user password'''
    route = '/reset_password'
    url = protocol + domain + port + route
    expected_response = {"email": email, "message": "Password updated"}

    response = requests.put(url, data={
        'email': email, 'reset_token': reset_token,
        'new_password': password
    })

    assert response.status_code == 200
    assert json.loads(response.text) == expected_response


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
