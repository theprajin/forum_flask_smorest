from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.extensions import db
from src.constants import URL_PREFIX
from src.posts.crud import get_post_or_404
from src.posts.exceptions import PostNotFound
from .schemas import PostViewResponse, PostViewCreate
from .models import PostView
from .crud import create_post_view

post_view_blp = Blueprint(
    "PostView",
    __name__,
    url_prefix=f"{URL_PREFIX}/",
)


@post_view_blp.route("posts/<int:post_id>/views")
class PostView(MethodView):

    @post_view_blp.response(200, PostViewResponse)
    def get(self, post_id):
        """Get Views List"""
        try:
            post = get_post_or_404(post_id)
            return PostView.query.all()
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except Exception as e:
            return str(e)

    @post_view_blp.arguments(PostViewCreate)
    @post_view_blp.response(201, PostViewResponse)
    def post(self, new_data, post_id):
        """Create Post View"""
        try:
            post = get_post_or_404(post_id)

            user = new_data.get("user_id")
            print(user)
            if user == 0:
                print("we are here")
                return jsonify({"message": "User ID cannot be zero"}), 400
            if post.user_id == user:
                return jsonify({"message": "You cannot view your own post"}), 400
            post_view = PostView(post_id=post_id)
            if post_view.user_id == user:
                abort(409, message="You already viewed this post")
            create_post_view(post_view)
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except Exception as e:
            return str(e)


# POST -> /posts/{post_id}/views
# GET -> /posts/{post_id}/views
# GET -> /users/{user_id}/views
