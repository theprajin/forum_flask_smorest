from flask import g
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from .schemas import (
    CommentResponse,
    CommentCreate,
    CommentUpdate,
    CommentDetailResponse,
)
from .crud import (
    get_comment_list,
    get_comment_or_404,
    create_comment,
    update_comment,
    delete_comment,
)
from .exceptions import CommentNotFound
from src.posts.crud import get_post_or_404
from src.posts.exceptions import PostNotFound
from src.constants import URL_PREFIX
from src.common.dependencies import load_user_from_request
from src.common.exceptions import UnauthorizedAccess

comment_blp = Blueprint(
    "Comments",
    __name__,
    url_prefix=f"{URL_PREFIX}/comments",
)


@comment_blp.route("/")
class Comment(MethodView):
    __model__ = "comments"

    @comment_blp.response(200, CommentResponse(many=True))
    def get(self):
        """Get Comment List"""
        return get_comment_list()

    @comment_blp.arguments(CommentCreate)
    @comment_blp.response(201, CommentResponse)
    @load_user_from_request
    def post(self, comment_data):
        """Create Comment"""
        try:
            user_id = g.get("current_user").id
            post_id = comment_data.get("post_id")
            get_post_or_404(post_id)
            comment = create_comment(comment_data, user_id)
            return comment
        except PostNotFound:
            abort(404, message=f"Post with ID '{post_id}' not found")
        except Exception as e:
            return str(e)


@comment_blp.route("/<int:comment_id>")
class CommentByID(MethodView):
    __model__ = "comments"

    @comment_blp.response(200, CommentDetailResponse)
    def get(self, comment_id):
        """Get Comment"""
        try:
            return get_comment_or_404(comment_id)
        except CommentNotFound:
            abort(404, message=f"Comment with ID '{comment_id}' not found")
        except Exception as e:
            return str(e)

    @comment_blp.arguments(CommentUpdate)
    @comment_blp.response(200, CommentResponse)
    @load_user_from_request
    def patch(self, comment_data, comment_id):
        """Update Comment"""
        try:
            comment = get_comment_or_404(comment_id)
            if comment.user_id == g.get("current_user").id or g.get("has_permission"):
                comment.content = comment_data.get("content") or comment.content
                return update_comment(comment)
            raise UnauthorizedAccess
        except CommentNotFound:
            abort(404, message=f"Comment with ID '{comment_id}' not found")
        except UnauthorizedAccess:
            abort(401, message="You are unauthorized to update the comment")
        except Exception as e:
            return str(e)

    @comment_blp.response(204)
    @load_user_from_request
    def delete(self, comment_id):
        """Delete Comment"""
        try:
            comment = get_comment_or_404(comment_id)
            if comment.user_id == g.get("current_user").id or g.get("has_permission"):
                delete_comment(comment_id)
            raise UnauthorizedAccess
        except CommentNotFound:
            abort(404, message=f"Comment with ID '{comment_id}' not found")
        except UnauthorizedAccess:
            abort(401, message="You are unauthorized to delete the comment")
        except Exception as e:
            return str(e)
