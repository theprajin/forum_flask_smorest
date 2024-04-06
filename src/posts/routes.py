from flask import jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from .schemas import PostCreate, PostResponse, PostUpdate, PostQuery
from .crud import get_post_or_404, get_post_list, create_post, update_post, delete_post
from .exceptions import PostNotFound
from .service import get_posts
from src.constants import URL_PREFIX
from src.categories.crud import get_category_or_404
from src.categories.exceptions import CategoryNotFound
from src.common.dependencies import load_user_from_request
from src.common.exceptions import UnauthorizedAccess

post_blp = Blueprint(
    "Posts",
    __name__,
    url_prefix=f"{URL_PREFIX}/posts",
)


@post_blp.route("/")
class Post(MethodView):
    @post_blp.arguments(PostQuery, location="query")
    @post_blp.response(200, PostResponse(many=True))
    def get(self, queries):
        """Get Post List"""
        # return get_post_list()
        return get_posts(queries)

    @post_blp.arguments(PostCreate)
    @post_blp.response(201, PostResponse)
    @load_user_from_request
    def post(self, post_data):
        """Create Post"""
        try:
            user_id = g.get("current_user").id
            print(user_id)
            category_id = post_data.get("category_id")
            get_category_or_404(category_id)
            post = create_post(post_data, user_id)
            return post
        except CategoryNotFound:
            abort(404, message=f"Category with ID '{category_id}' not found")
        except Exception as e:
            return str(e)


@post_blp.route("/<int:post_id>")
class PostByID(MethodView):
    @post_blp.response(200, PostResponse)
    def get(self, post_id):
        """Get Post"""
        try:
            return get_post_or_404(post_id)
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except Exception as e:
            return str(e)

    @post_blp.arguments(PostUpdate)
    @post_blp.response(200, PostResponse)
    @load_user_from_request
    def patch(self, post_data, post_id):
        """Update Post"""
        try:
            post = get_post_or_404(post_id)
            if post.user_id != g.get("current_user").id:
                abort(401, message="You are unauthorized to update this post")
            post.title = post_data.get("title") or post.title
            post.content = post_data.get("content") or post.content
            return update_post(post)
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except Exception as e:
            return str(e)

    @post_blp.response(204)
    @load_user_from_request
    def delete(self, post_id):
        """Delete Post"""
        try:
            post = get_post_or_404(post_id)
            if post.user_id != g.get("current_user").id:
                abort(401, message="You are unauthorized to delete this post")

            return delete_post(post_id)
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except Exception as e:
            return str(e)
