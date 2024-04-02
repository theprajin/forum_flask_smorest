from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from .schemas import PostSchema, PostCreateSchema, PostResponseSchema
from .crud import get_post_or_404, get_post_list, create_post, update_post, delete_post
from src.constants import URL_PREFIX
from .exceptions import PostNotFound

post_blp = Blueprint(
    "Posts",
    __name__,
    url_prefix=URL_PREFIX,
)


@post_blp.route("/")
class Post(MethodView):
    @post_blp.response(200, PostResponseSchema(many=True))
    def get(self):
        """Get Post List"""
        return get_post_list()

    @post_blp.arguments(PostCreateSchema)
    @post_blp.response(201, PostResponseSchema)
    def post(self, post_data):
        """Create Post"""
        post = create_post(post_data)
        return post


@post_blp.route("/<int:post_id>")
class PostByID(MethodView):
    @post_blp.response(200, PostResponseSchema)
    def get(self, post_id):
        """Get Post"""
        try:
            return get_post_or_404(post_id)
        except PostNotFound:
            abort(404, message=f"Post with ID {post_id} not found")
        except Exception as e:
            return str(e)

    @post_blp.arguments(PostSchema)
    @post_blp.response(200, PostResponseSchema)
    def patch(self, post_data, post_id):
        """Update Post"""
        try:
            post = get_post_or_404(post_id)
            post.title = post_data.get("title") or post.title
            post.content = post_data.get("content") or post.content
            return update_post(post)
        except PostNotFound:
            abort(404, message=f"Post with ID {post_id} not found")
        except Exception as e:
            return str(e)

    @post_blp.response(204)
    def delete(self, post_id):
        """Delete Post"""
        try:
            get_post_or_404(post_id)

            return delete_post(post_id)
        except PostNotFound:
            abort(404, message=f"Post with ID {post_id} not found")
        except Exception as e:
            return str(e)
