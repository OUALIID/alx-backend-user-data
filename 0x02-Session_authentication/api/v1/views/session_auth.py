from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Authenticate user and create session."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.search({"email": email})

    if not user:
        return jsonify({"error": "No user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "Wrong password"}), 401

    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "Failed to create session"}), 500

    session_name = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)
    return response


@app_views.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """Delete user session."""
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
