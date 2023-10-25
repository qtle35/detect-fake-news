from flask import request, jsonify, session
from factory import db, bcrypt
from routes import blueprint
from auth.user import User
import json

@blueprint.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = User.check_login(username, password)
    if user:
        return json.dumps({ username: username, password: password }), 200
    return jsonify({"message": "Authorized"}), 401
