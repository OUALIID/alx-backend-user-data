#!/usr/bin/env python3
"""
user authentication service
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def welcom():
    """Handler for the root URL."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """The users function that implements the POST /users path."""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """Login function to respond to the POST /sessions path."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        if AUTH.valid_login(email, password):
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", AUTH.create_session(email))
            return response
        else:
            abort(401)
    except NoResultFound:
        abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """Log out the user."""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """Profile function to respond to the profile path."""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
