#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
