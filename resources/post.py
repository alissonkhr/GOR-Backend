import models

from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

posts = Blueprint("posts", "posts")

# GET DISCUSSIONS
@posts.route("/", methods=["GET"])
def discussion_index():
    try:
        posts_dicts = [model_to_dict(post) for post in models.UserPost.select()]
        for post_dict in posts_dicts:
            post_dict["user"].pop("password")
        print(posts_dicts)
        return jsonify(
            data=posts_dicts,
            status={"code": 200, "message": "Successfully found posts."},
        )
    except models.DoesNotExist:
        return jsonify(
            data={}, status={"code": 401, "message": "Error finding the posts."}
        )


# CREATE DISCUSSIONS
@posts.route("/", methods=["POST"])
@login_required
def create_discussion():
    payload = request.get_json()
    post = models.UserPost.create(
        game=payload["game"], user=current_user.id, message=payload["message"]
    )
    post_dict = model_to_dict(post)
    post_dict["user"].pop("password")
    return jsonify(
        data=post_dict, status={"code": 201, "message": "Successfully created a post."}
    )
