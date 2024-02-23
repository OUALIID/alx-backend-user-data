#!/usr/bin/env python3
"""
Solution for user authentication service
"""
import requests
from auth import Auth


def register_user(email: str, password: str) -> None:
    """A test for the function that registers a user."""
    response = requests.post(
        "http://localhost:5000/users", {"password": password, "email": email}
    )
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "") == "application/json"
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """A test for the function that does the login verification."""
    response = requests.post(
        "http://localhost:5000/sessions",
        {"password": password, "email": email}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """A test for the function that does the login."""
    response = requests.post(
        "http://localhost:5000/sessions",
        {"password": password, "email": email}
    )
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "") == "application/json"
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """A test for the function that treats the logout."""
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """A test for the function that checks the logged."""
    response = requests.get(
        "http://localhost:5000/profile", cookies={"session_id": session_id}
    )
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """A test for the function that checks the logout."""
    response = requests.get(
        "http://localhost:5000/logout", cookies={"session_id": session_id}
    )
    assert response.status_code != 403


def reset_password_token(email: str) -> str:
    """A test for the function that resets the password token."""
    response = requests.post("http://localhost:5000/reset_password",
                             {"email": email})
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """A test for the function that updates a password."""
    response = requests.put(
        "http://localhost:5000/reset_password",
        {"email": email,
         "reset_token": reset_token,
         "new_password": new_password},
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


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
