import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint("users", "user")


@user.route("/register", methods=["POST"])
def register():
    payload = request.get_json()

    payload["username"] = payload["username"].lower()
    try:
        models.User.get(models.User.username == payload["username"])
        return jsonify(
            data={},
            status={"code": 401, "message": "A user with that name already exists."},
        )
    except models.DoesNotExist:
        payload["password"] = generate_password_hash(payload["password"])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)
        del user_dict["password"]

        return jsonify(data=user_dict, status={"code": 201, "message": "Success!"}), 201


@user.route("/login", methods=["POST"])
def login():
    payload = request.get_json()

    payload["username"] = payload["username"].lower()
    try:
        user = models.User.get(models.User.username == payload["username"])
        user_dict = model_to_dict(user)
        if check_password_hash(user_dict["password"], payload["password"]):
            del user_dict["password"]
            login_user(user)
            return (
                jsonify(
                    data=user_dict,
                    status={"code": 200, "message": "User successfully logged in!"},
                ),
                200,
            )
        else:
            return (
                jsonify(
                    data={},
                    status={
                        "code": 401,
                        "message": "Username or Password do not match.",
                    },
                ),
                401,
            )
    except models.DoesNotExist:
        return (
            jsonify(
                data={},
                status={"code": 401, "message": "Username or Password do not match."},
            ),
            401,
        )


@user.route("/logout", methods=["GET"])
def logout():
    logout_user()

    return jsonify(data={}, status=200, message="Successfully logged out."), 200
