from flask import request, jsonify, session
from factory import db, bcrypt
from routes import blueprint
from auth.user import User

@blueprint.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    if not User.check_login(username, password):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"message": "Authorized"}), 200