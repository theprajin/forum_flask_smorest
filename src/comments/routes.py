from flask_smorest import Blueprint, abort
from flask.views import MethodView

from .schemas import CommentResponse, CommentCreate, CommentUpdate
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

comment_blp = Blueprint(
    "Comments",
    __name__,
    url_prefix="/comments",
)


@comment_blp.route("/")
class Comment(MethodView):

    @comment_blp.response(200, CommentResponse(many=True))
    def get(self):
        """Get Comment List"""
        return get_comment_list()

    @comment_blp.arguments(CommentCreate)
    @comment_blp.response(201, CommentResponse)
    def post(self, comment_data):
        """Create Comment"""
        try:
            post_id = comment_data.get("post_id")
            get_post_or_404(post_id)
            comment = create_comment(comment_data)
            return comment
        except PostNotFound:
            abort(404, message=f"Post with ID {post_id} not found")
        except Exception as e:
            return str(e)


@comment_blp.route("/<int:comment_id>")
class CommentByID(MethodView):

    @comment_blp.response(200, CommentResponse)
    def get(self, comment_id):
        """Get Comment"""
        try:
            return get_comment_or_404(comment_id)
        except CommentNotFound:
            abort(404, message=f"Comment with ID {comment_id} not found")
        except Exception as e:
            return str(e)

    @comment_blp.arguments(CommentUpdate)
    @comment_blp.response(200, CommentResponse)
    def patch(self, comment_data, comment_id):
        """Update Comment"""
        try:
            comment = get_comment_or_404(comment_id)
            comment.content = comment_data.get("content") or comment.content
            return update_comment(comment)
        except CommentNotFound:
            abort(404, message=f"Comment with ID {comment_id} not found")
        except Exception as e:
            return str(e)

    @comment_blp.response(204)
    def delete(self, comment_id):
        """Delete Comment"""
        try:
            get_comment_or_404(comment_id)
            delete_comment(comment_id)
        except CommentNotFound:
            abort(404, message=f"Comment with ID {comment_id} not found")
        except Exception as e:
            return str(e)
