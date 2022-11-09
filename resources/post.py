import models

from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

posts = Blueprint("posts", "posts")

# GET ALL DISCUSSIONS (anyone can see these)
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


# CREATE DISCUSSIONS (only users that are logged in)
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


# GET A DISCUSSION (anyone can see these)
@posts.route("/<id>", methods=["GET"])
def get_one_post(id):
    try:
        post = models.UserPost.get_by_id(id)
        post_dict = model_to_dict(post)
        post_dict["user"].pop("password")
        return jsonify(
            data=post_dict,
            status={"code": 200, "message": "Successfully found this post."},
        )
    except models.DoesNotExist:
        return jsonify(
            data={}, status={"code": 401, "message": "Error finding the posts."}
        )


# UPDATE A DISCUSSION (only users that are logged in)
# FIX THE ISSUE WITH ANY USER BEING ABLE TO UPDATE
# SO CURRENT USER CAN ONLY UPDATE THEIR OWN
@posts.route("/<id>", methods=["PUT"])
@login_required
def update_post(id):
    payload = request.get_json()
    query = models.UserPost.update(**payload).where(models.UserPost.id == id)
    query.execute()
    post = model_to_dict(models.UserPost.get_by_id(id))
    post["user"].pop("password")
    return (
        jsonify(
            data=post,
            status=200,
            message="Post updated successfully.",
        ),
        200,
    )


# DELETE A DISCUSSION (only users that are logged in)
# WORKING BUT SOME ERRORS SOMEHOW????
@posts.route("/<id>", methods=["DELETE"])
@login_required
def delete_post(id):
    query = models.UserPost.delete().where(models.UserPost.id == id)
    query.execute()
    return (
        jsonify(
            data=model_to_dict(models.UserPost.get_by_id(id)),
            message="Successfully deleted",
            status=200,
        ),
        200,
    )
